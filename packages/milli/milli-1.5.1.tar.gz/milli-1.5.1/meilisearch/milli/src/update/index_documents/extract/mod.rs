mod extract_docid_word_positions;
mod extract_facet_number_docids;
mod extract_facet_string_docids;
mod extract_fid_docid_facet_values;
mod extract_fid_word_count_docids;
mod extract_geo_points;
mod extract_vector_points;
mod extract_word_docids;
mod extract_word_fid_docids;
mod extract_word_pair_proximity_docids;
mod extract_word_position_docids;

use std::collections::HashSet;
use std::fs::File;
use std::io::BufReader;

use crossbeam_channel::Sender;
use log::debug;
use rayon::prelude::*;

use self::extract_docid_word_positions::extract_docid_word_positions;
use self::extract_facet_number_docids::extract_facet_number_docids;
use self::extract_facet_string_docids::extract_facet_string_docids;
use self::extract_fid_docid_facet_values::{extract_fid_docid_facet_values, ExtractedFacetValues};
use self::extract_fid_word_count_docids::extract_fid_word_count_docids;
use self::extract_geo_points::extract_geo_points;
use self::extract_vector_points::extract_vector_points;
use self::extract_word_docids::extract_word_docids;
use self::extract_word_fid_docids::extract_word_fid_docids;
use self::extract_word_pair_proximity_docids::extract_word_pair_proximity_docids;
use self::extract_word_position_docids::extract_word_position_docids;
use super::helpers::{
    as_cloneable_grenad, merge_cbo_roaring_bitmaps, merge_roaring_bitmaps, CursorClonableMmap,
    GrenadParameters, MergeFn, MergeableReader,
};
use super::{helpers, TypedChunk};
use crate::{FieldId, Result};

/// Extract data for each databases from obkv documents in parallel.
/// Send data in grenad file over provided Sender.
#[allow(clippy::too_many_arguments)]
pub(crate) fn data_from_obkv_documents(
    original_obkv_chunks: impl Iterator<Item = Result<grenad::Reader<BufReader<File>>>> + Send,
    flattened_obkv_chunks: impl Iterator<Item = Result<grenad::Reader<BufReader<File>>>> + Send,
    indexer: GrenadParameters,
    lmdb_writer_sx: Sender<Result<TypedChunk>>,
    searchable_fields: Option<HashSet<FieldId>>,
    faceted_fields: HashSet<FieldId>,
    primary_key_id: FieldId,
    geo_fields_ids: Option<(FieldId, FieldId)>,
    vectors_field_id: Option<FieldId>,
    stop_words: Option<fst::Set<&[u8]>>,
    allowed_separators: Option<&[&str]>,
    dictionary: Option<&[&str]>,
    max_positions_per_attributes: Option<u32>,
    exact_attributes: HashSet<FieldId>,
) -> Result<()> {
    puffin::profile_function!();

    original_obkv_chunks
        .par_bridge()
        .map(|original_documents_chunk| {
            send_original_documents_data(
                original_documents_chunk,
                indexer,
                lmdb_writer_sx.clone(),
                vectors_field_id,
                primary_key_id,
            )
        })
        .collect::<Result<()>>()?;

    #[allow(clippy::type_complexity)]
    let result: Result<(Vec<_>, (Vec<_>, (Vec<_>, (Vec<_>, (Vec<_>, Vec<_>)))))> =
        flattened_obkv_chunks
            .par_bridge()
            .map(|flattened_obkv_chunks| {
                send_and_extract_flattened_documents_data(
                    flattened_obkv_chunks,
                    indexer,
                    lmdb_writer_sx.clone(),
                    &searchable_fields,
                    &faceted_fields,
                    primary_key_id,
                    geo_fields_ids,
                    &stop_words,
                    &allowed_separators,
                    &dictionary,
                    max_positions_per_attributes,
                )
            })
            .collect();

    let (
        docid_word_positions_chunks,
        (
            docid_fid_facet_numbers_chunks,
            (
                docid_fid_facet_strings_chunks,
                (
                    facet_is_null_docids_chunks,
                    (facet_is_empty_docids_chunks, facet_exists_docids_chunks),
                ),
            ),
        ),
    ) = result?;

    // merge facet_exists_docids and send them as a typed chunk
    {
        let lmdb_writer_sx = lmdb_writer_sx.clone();
        rayon::spawn(move || {
            debug!("merge {} database", "facet-id-exists-docids");
            match facet_exists_docids_chunks.merge(merge_cbo_roaring_bitmaps, &indexer) {
                Ok(reader) => {
                    let _ = lmdb_writer_sx.send(Ok(TypedChunk::FieldIdFacetExistsDocids(reader)));
                }
                Err(e) => {
                    let _ = lmdb_writer_sx.send(Err(e));
                }
            }
        });
    }

    // merge facet_is_null_docids and send them as a typed chunk
    {
        let lmdb_writer_sx = lmdb_writer_sx.clone();
        rayon::spawn(move || {
            debug!("merge {} database", "facet-id-is-null-docids");
            match facet_is_null_docids_chunks.merge(merge_cbo_roaring_bitmaps, &indexer) {
                Ok(reader) => {
                    let _ = lmdb_writer_sx.send(Ok(TypedChunk::FieldIdFacetIsNullDocids(reader)));
                }
                Err(e) => {
                    let _ = lmdb_writer_sx.send(Err(e));
                }
            }
        });
    }

    // merge facet_is_empty_docids and send them as a typed chunk
    {
        let lmdb_writer_sx = lmdb_writer_sx.clone();
        rayon::spawn(move || {
            debug!("merge {} database", "facet-id-is-empty-docids");
            match facet_is_empty_docids_chunks.merge(merge_cbo_roaring_bitmaps, &indexer) {
                Ok(reader) => {
                    let _ = lmdb_writer_sx.send(Ok(TypedChunk::FieldIdFacetIsEmptyDocids(reader)));
                }
                Err(e) => {
                    let _ = lmdb_writer_sx.send(Err(e));
                }
            }
        });
    }

    spawn_extraction_task::<_, _, Vec<grenad::Reader<BufReader<File>>>>(
        docid_word_positions_chunks.clone(),
        indexer,
        lmdb_writer_sx.clone(),
        extract_word_pair_proximity_docids,
        merge_cbo_roaring_bitmaps,
        TypedChunk::WordPairProximityDocids,
        "word-pair-proximity-docids",
    );

    spawn_extraction_task::<_, _, Vec<grenad::Reader<BufReader<File>>>>(
        docid_word_positions_chunks.clone(),
        indexer,
        lmdb_writer_sx.clone(),
        extract_fid_word_count_docids,
        merge_cbo_roaring_bitmaps,
        TypedChunk::FieldIdWordcountDocids,
        "field-id-wordcount-docids",
    );

    spawn_extraction_task::<
        _,
        _,
        Vec<(grenad::Reader<BufReader<File>>, grenad::Reader<BufReader<File>>)>,
    >(
        docid_word_positions_chunks.clone(),
        indexer,
        lmdb_writer_sx.clone(),
        move |doc_word_pos, indexer| extract_word_docids(doc_word_pos, indexer, &exact_attributes),
        merge_roaring_bitmaps,
        |(word_docids_reader, exact_word_docids_reader)| TypedChunk::WordDocids {
            word_docids_reader,
            exact_word_docids_reader,
        },
        "word-docids",
    );

    spawn_extraction_task::<_, _, Vec<grenad::Reader<BufReader<File>>>>(
        docid_word_positions_chunks.clone(),
        indexer,
        lmdb_writer_sx.clone(),
        extract_word_position_docids,
        merge_cbo_roaring_bitmaps,
        TypedChunk::WordPositionDocids,
        "word-position-docids",
    );
    spawn_extraction_task::<_, _, Vec<grenad::Reader<BufReader<File>>>>(
        docid_word_positions_chunks,
        indexer,
        lmdb_writer_sx.clone(),
        extract_word_fid_docids,
        merge_cbo_roaring_bitmaps,
        TypedChunk::WordFidDocids,
        "word-fid-docids",
    );

    spawn_extraction_task::<_, _, Vec<grenad::Reader<BufReader<File>>>>(
        docid_fid_facet_strings_chunks,
        indexer,
        lmdb_writer_sx.clone(),
        extract_facet_string_docids,
        merge_cbo_roaring_bitmaps,
        TypedChunk::FieldIdFacetStringDocids,
        "field-id-facet-string-docids",
    );

    spawn_extraction_task::<_, _, Vec<grenad::Reader<BufReader<File>>>>(
        docid_fid_facet_numbers_chunks,
        indexer,
        lmdb_writer_sx,
        extract_facet_number_docids,
        merge_cbo_roaring_bitmaps,
        TypedChunk::FieldIdFacetNumberDocids,
        "field-id-facet-number-docids",
    );

    Ok(())
}

/// Spawn a new task to extract data for a specific DB using extract_fn.
/// Generated grenad chunks are merged using the merge_fn.
/// The result of merged chunks is serialized as TypedChunk using the serialize_fn
/// and sent into lmdb_writer_sx.
fn spawn_extraction_task<FE, FS, M>(
    chunks: Vec<grenad::Reader<CursorClonableMmap>>,
    indexer: GrenadParameters,
    lmdb_writer_sx: Sender<Result<TypedChunk>>,
    extract_fn: FE,
    merge_fn: MergeFn,
    serialize_fn: FS,
    name: &'static str,
) where
    FE: Fn(grenad::Reader<CursorClonableMmap>, GrenadParameters) -> Result<M::Output>
        + Sync
        + Send
        + 'static,
    FS: Fn(M::Output) -> TypedChunk + Sync + Send + 'static,
    M: MergeableReader + FromParallelIterator<M::Output> + Send + 'static,
    M::Output: Send,
{
    rayon::spawn(move || {
        puffin::profile_scope!("extract_multiple_chunks", name);
        let chunks: Result<M> =
            chunks.into_par_iter().map(|chunk| extract_fn(chunk, indexer)).collect();
        rayon::spawn(move || match chunks {
            Ok(chunks) => {
                debug!("merge {} database", name);
                puffin::profile_scope!("merge_multiple_chunks", name);
                let reader = chunks.merge(merge_fn, &indexer);
                let _ = lmdb_writer_sx.send(reader.map(serialize_fn));
            }
            Err(e) => {
                let _ = lmdb_writer_sx.send(Err(e));
            }
        })
    });
}

/// Extract chunked data and send it into lmdb_writer_sx sender:
/// - documents
fn send_original_documents_data(
    original_documents_chunk: Result<grenad::Reader<BufReader<File>>>,
    indexer: GrenadParameters,
    lmdb_writer_sx: Sender<Result<TypedChunk>>,
    vectors_field_id: Option<FieldId>,
    primary_key_id: FieldId,
) -> Result<()> {
    let original_documents_chunk =
        original_documents_chunk.and_then(|c| unsafe { as_cloneable_grenad(&c) })?;

    if let Some(vectors_field_id) = vectors_field_id {
        let documents_chunk_cloned = original_documents_chunk.clone();
        let lmdb_writer_sx_cloned = lmdb_writer_sx.clone();
        rayon::spawn(move || {
            let result = extract_vector_points(
                documents_chunk_cloned,
                indexer,
                primary_key_id,
                vectors_field_id,
            );
            let _ = match result {
                Ok(vector_points) => {
                    lmdb_writer_sx_cloned.send(Ok(TypedChunk::VectorPoints(vector_points)))
                }
                Err(error) => lmdb_writer_sx_cloned.send(Err(error)),
            };
        });
    }

    // TODO: create a custom internal error
    lmdb_writer_sx.send(Ok(TypedChunk::Documents(original_documents_chunk))).unwrap();
    Ok(())
}

/// Extract chunked data and send it into lmdb_writer_sx sender:
/// - documents_ids
/// - docid_word_positions
/// - docid_fid_facet_numbers
/// - docid_fid_facet_strings
/// - docid_fid_facet_exists
#[allow(clippy::too_many_arguments)]
#[allow(clippy::type_complexity)]
fn send_and_extract_flattened_documents_data(
    flattened_documents_chunk: Result<grenad::Reader<BufReader<File>>>,
    indexer: GrenadParameters,
    lmdb_writer_sx: Sender<Result<TypedChunk>>,
    searchable_fields: &Option<HashSet<FieldId>>,
    faceted_fields: &HashSet<FieldId>,
    primary_key_id: FieldId,
    geo_fields_ids: Option<(FieldId, FieldId)>,
    stop_words: &Option<fst::Set<&[u8]>>,
    allowed_separators: &Option<&[&str]>,
    dictionary: &Option<&[&str]>,
    max_positions_per_attributes: Option<u32>,
) -> Result<(
    grenad::Reader<CursorClonableMmap>,
    (
        grenad::Reader<CursorClonableMmap>,
        (
            grenad::Reader<CursorClonableMmap>,
            (
                grenad::Reader<BufReader<File>>,
                (grenad::Reader<BufReader<File>>, grenad::Reader<BufReader<File>>),
            ),
        ),
    ),
)> {
    let flattened_documents_chunk =
        flattened_documents_chunk.and_then(|c| unsafe { as_cloneable_grenad(&c) })?;

    if let Some(geo_fields_ids) = geo_fields_ids {
        let documents_chunk_cloned = flattened_documents_chunk.clone();
        let lmdb_writer_sx_cloned = lmdb_writer_sx.clone();
        rayon::spawn(move || {
            let result =
                extract_geo_points(documents_chunk_cloned, indexer, primary_key_id, geo_fields_ids);
            let _ = match result {
                Ok(geo_points) => lmdb_writer_sx_cloned.send(Ok(TypedChunk::GeoPoints(geo_points))),
                Err(error) => lmdb_writer_sx_cloned.send(Err(error)),
            };
        });
    }

    let (docid_word_positions_chunk, docid_fid_facet_values_chunks): (Result<_>, Result<_>) =
        rayon::join(
            || {
                let (documents_ids, docid_word_positions_chunk, script_language_pair) =
                    extract_docid_word_positions(
                        flattened_documents_chunk.clone(),
                        indexer,
                        searchable_fields,
                        stop_words.as_ref(),
                        *allowed_separators,
                        *dictionary,
                        max_positions_per_attributes,
                    )?;

                // send documents_ids to DB writer
                let _ = lmdb_writer_sx.send(Ok(TypedChunk::NewDocumentsIds(documents_ids)));

                // send docid_word_positions_chunk to DB writer
                let docid_word_positions_chunk =
                    unsafe { as_cloneable_grenad(&docid_word_positions_chunk)? };

                let _ =
                    lmdb_writer_sx.send(Ok(TypedChunk::ScriptLanguageDocids(script_language_pair)));

                Ok(docid_word_positions_chunk)
            },
            || {
                let ExtractedFacetValues {
                    docid_fid_facet_numbers_chunk,
                    docid_fid_facet_strings_chunk,
                    fid_facet_is_null_docids_chunk,
                    fid_facet_is_empty_docids_chunk,
                    fid_facet_exists_docids_chunk,
                } = extract_fid_docid_facet_values(
                    flattened_documents_chunk.clone(),
                    indexer,
                    faceted_fields,
                    geo_fields_ids,
                )?;

                // send docid_fid_facet_numbers_chunk to DB writer
                let docid_fid_facet_numbers_chunk =
                    unsafe { as_cloneable_grenad(&docid_fid_facet_numbers_chunk)? };

                let _ = lmdb_writer_sx.send(Ok(TypedChunk::FieldIdDocidFacetNumbers(
                    docid_fid_facet_numbers_chunk.clone(),
                )));

                // send docid_fid_facet_strings_chunk to DB writer
                let docid_fid_facet_strings_chunk =
                    unsafe { as_cloneable_grenad(&docid_fid_facet_strings_chunk)? };

                let _ = lmdb_writer_sx.send(Ok(TypedChunk::FieldIdDocidFacetStrings(
                    docid_fid_facet_strings_chunk.clone(),
                )));

                Ok((
                    docid_fid_facet_numbers_chunk,
                    (
                        docid_fid_facet_strings_chunk,
                        (
                            fid_facet_is_null_docids_chunk,
                            (fid_facet_is_empty_docids_chunk, fid_facet_exists_docids_chunk),
                        ),
                    ),
                ))
            },
        );

    Ok((docid_word_positions_chunk?, docid_fid_facet_values_chunks?))
}
