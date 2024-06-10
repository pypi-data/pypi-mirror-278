use std::collections::HashMap;
use std::convert::TryInto;
use std::fs::File;
use std::io::{self, BufReader};

use bytemuck::allocation::pod_collect_to_vec;
use charabia::{Language, Script};
use grenad::{Merger, MergerBuilder};
use heed::types::Bytes;
use heed::RwTxn;
use obkv::{KvReader, KvWriter};
use roaring::RoaringBitmap;

use super::helpers::{
    self, keep_first, merge_deladd_btreeset_string, merge_deladd_cbo_roaring_bitmaps,
    merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap, merge_ignore_values, valid_lmdb_key,
    CursorClonableMmap,
};
use super::MergeFn;
use crate::external_documents_ids::{DocumentOperation, DocumentOperationKind};
use crate::facet::FacetType;
use crate::index::db_name::DOCUMENTS;
use crate::update::del_add::{deladd_serialize_add_side, DelAdd, KvReaderDelAdd};
use crate::update::facet::FacetsUpdate;
use crate::update::index_documents::helpers::{
    as_cloneable_grenad, keep_latest_obkv, try_split_array_at,
};
use crate::{
    lat_lng_to_xyz, DocumentId, FieldId, GeoPoint, Index, InternalError, Result, SerializationError,
};

/// This struct accumulates and group the TypedChunks
/// and is able to give the biggest accumulated group to index them all together
/// with a merger.
#[derive(Default)]
pub(crate) struct ChunkAccumulator {
    inner: Vec<Vec<TypedChunk>>,
}

impl ChunkAccumulator {
    pub fn pop_longest(&mut self) -> Option<Vec<TypedChunk>> {
        match self.inner.iter().max_by_key(|v| v.len()) {
            Some(left) => {
                let position = self.inner.iter().position(|right| left.len() == right.len());
                position.map(|p| self.inner.remove(p)).filter(|v| !v.is_empty())
            }
            None => None,
        }
    }

    pub fn insert(&mut self, chunk: TypedChunk) {
        match self
            .inner
            .iter()
            .position(|right| right.first().map_or(false, |right| chunk.mergeable_with(right)))
        {
            Some(position) => {
                let v = self.inner.get_mut(position).unwrap();
                v.push(chunk);
            }
            None => self.inner.push(vec![chunk]),
        }
    }
}

pub(crate) enum TypedChunk {
    FieldIdDocidFacetStrings(grenad::Reader<CursorClonableMmap>),
    FieldIdDocidFacetNumbers(grenad::Reader<CursorClonableMmap>),
    Documents(grenad::Reader<CursorClonableMmap>),
    FieldIdWordCountDocids(grenad::Reader<BufReader<File>>),
    WordDocids {
        word_docids_reader: grenad::Reader<BufReader<File>>,
        exact_word_docids_reader: grenad::Reader<BufReader<File>>,
        word_fid_docids_reader: grenad::Reader<BufReader<File>>,
    },
    WordPositionDocids(grenad::Reader<BufReader<File>>),
    WordPairProximityDocids(grenad::Reader<BufReader<File>>),
    FieldIdFacetStringDocids((grenad::Reader<BufReader<File>>, grenad::Reader<BufReader<File>>)),
    FieldIdFacetNumberDocids(grenad::Reader<BufReader<File>>),
    FieldIdFacetExistsDocids(grenad::Reader<BufReader<File>>),
    FieldIdFacetIsNullDocids(grenad::Reader<BufReader<File>>),
    FieldIdFacetIsEmptyDocids(grenad::Reader<BufReader<File>>),
    GeoPoints(grenad::Reader<BufReader<File>>),
    VectorPoints {
        remove_vectors: grenad::Reader<BufReader<File>>,
        embeddings: Option<grenad::Reader<BufReader<File>>>,
        expected_dimension: usize,
        manual_vectors: grenad::Reader<BufReader<File>>,
        embedder_name: String,
    },
    ScriptLanguageDocids(HashMap<(Script, Language), (RoaringBitmap, RoaringBitmap)>),
}

impl TypedChunk {
    fn mergeable_with(&self, other: &Self) -> bool {
        use TypedChunk::*;
        match (self, other) {
            (FieldIdDocidFacetStrings(_), FieldIdDocidFacetStrings(_))
            | (FieldIdDocidFacetNumbers(_), FieldIdDocidFacetNumbers(_))
            | (Documents(_), Documents(_))
            | (FieldIdWordCountDocids(_), FieldIdWordCountDocids(_))
            | (WordDocids { .. }, WordDocids { .. })
            | (WordPositionDocids(_), WordPositionDocids(_))
            | (WordPairProximityDocids(_), WordPairProximityDocids(_))
            | (FieldIdFacetStringDocids(_), FieldIdFacetStringDocids(_))
            | (FieldIdFacetNumberDocids(_), FieldIdFacetNumberDocids(_))
            | (FieldIdFacetExistsDocids(_), FieldIdFacetExistsDocids(_))
            | (FieldIdFacetIsNullDocids(_), FieldIdFacetIsNullDocids(_))
            | (FieldIdFacetIsEmptyDocids(_), FieldIdFacetIsEmptyDocids(_))
            | (GeoPoints(_), GeoPoints(_))
            | (ScriptLanguageDocids(_), ScriptLanguageDocids(_)) => true,
            (
                VectorPoints { embedder_name: left, expected_dimension: left_dim, .. },
                VectorPoints { embedder_name: right, expected_dimension: right_dim, .. },
            ) => left == right && left_dim == right_dim,
            _ => false,
        }
    }
}

impl TypedChunk {
    pub fn to_debug_string(&self) -> String {
        match self {
            TypedChunk::FieldIdDocidFacetStrings(grenad) => {
                format!("FieldIdDocidFacetStrings {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::FieldIdDocidFacetNumbers(grenad) => {
                format!("FieldIdDocidFacetNumbers {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::Documents(grenad) => {
                format!("Documents {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::FieldIdWordCountDocids(grenad) => {
                format!("FieldIdWordcountDocids {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::WordDocids {
                word_docids_reader,
                exact_word_docids_reader,
                word_fid_docids_reader,
            } => format!(
                "WordDocids {{ word_docids_reader: {}, exact_word_docids_reader: {}, word_fid_docids_reader: {} }}",
                word_docids_reader.len(),
                exact_word_docids_reader.len(),
                word_fid_docids_reader.len()
            ),
            TypedChunk::WordPositionDocids(grenad) => {
                format!("WordPositionDocids {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::WordPairProximityDocids(grenad) => {
                format!("WordPairProximityDocids {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::FieldIdFacetStringDocids((grenad, _)) => {
                format!("FieldIdFacetStringDocids {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::FieldIdFacetNumberDocids(grenad) => {
                format!("FieldIdFacetNumberDocids {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::FieldIdFacetExistsDocids(grenad) => {
                format!("FieldIdFacetExistsDocids {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::FieldIdFacetIsNullDocids(grenad) => {
                format!("FieldIdFacetIsNullDocids {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::FieldIdFacetIsEmptyDocids(grenad) => {
                format!("FieldIdFacetIsEmptyDocids {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::GeoPoints(grenad) => {
                format!("GeoPoints {{ number_of_entries: {} }}", grenad.len())
            }
            TypedChunk::VectorPoints{ remove_vectors, manual_vectors, embeddings, expected_dimension, embedder_name } => {
                format!("VectorPoints {{ remove_vectors: {}, manual_vectors: {}, embeddings: {}, dimension: {}, embedder_name: {} }}", remove_vectors.len(), manual_vectors.len(), embeddings.as_ref().map(|e| e.len()).unwrap_or_default(), expected_dimension, embedder_name)
            }
            TypedChunk::ScriptLanguageDocids(sl_map) => {
                format!("ScriptLanguageDocids {{ number_of_entries: {} }}", sl_map.len())
            }
        }
    }
}

/// Write typed chunk in the corresponding LMDB database of the provided index.
/// Return new documents seen.
#[tracing::instrument(level = "trace", skip_all, target = "indexing::write_db")]
pub(crate) fn write_typed_chunk_into_index(
    typed_chunks: Vec<TypedChunk>,
    index: &Index,
    wtxn: &mut RwTxn,
) -> Result<(RoaringBitmap, bool)> {
    puffin::profile_function!(typed_chunks[0].to_debug_string());

    let mut is_merged_database = false;
    match typed_chunks[0] {
        TypedChunk::Documents(_) => {
            let span = tracing::trace_span!(target: "indexing::write_db", "documents");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(keep_latest_obkv as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::Documents(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();
            let mut operations: Vec<DocumentOperation> = Default::default();

            let mut docids = index.documents_ids(wtxn)?;
            let mut iter = merger.into_stream_merger_iter()?;
            while let Some((key, reader)) = iter.next()? {
                let mut writer: KvWriter<_, FieldId> = KvWriter::memory();
                let reader: KvReader<FieldId> = KvReader::new(reader);

                let (document_id_bytes, external_id_bytes) = try_split_array_at(key)
                    .ok_or(SerializationError::Decoding { db_name: Some(DOCUMENTS) })?;
                let docid = DocumentId::from_be_bytes(document_id_bytes);
                let external_id = std::str::from_utf8(external_id_bytes)?;

                for (field_id, value) in reader.iter() {
                    let del_add_reader = KvReaderDelAdd::new(value);

                    if let Some(addition) = del_add_reader.get(DelAdd::Addition) {
                        writer.insert(field_id, addition)?;
                    }
                }

                let db = index.documents.remap_data_type::<Bytes>();

                if !writer.is_empty() {
                    db.put(wtxn, &docid, &writer.into_inner().unwrap())?;
                    operations.push(DocumentOperation {
                        external_id: external_id.to_string(),
                        internal_id: docid,
                        kind: DocumentOperationKind::Create,
                    });
                    docids.insert(docid);
                } else {
                    db.delete(wtxn, &docid)?;
                    operations.push(DocumentOperation {
                        external_id: external_id.to_string(),
                        internal_id: docid,
                        kind: DocumentOperationKind::Delete,
                    });
                    docids.remove(docid);
                }
            }
            let external_documents_docids = index.external_documents_ids();
            external_documents_docids.apply(wtxn, operations)?;
            index.put_documents_ids(wtxn, &docids)?;
        }
        TypedChunk::FieldIdWordCountDocids(_) => {
            let span =
                tracing::trace_span!(target: "indexing::write_db", "field_id_word_count_docids");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::FieldIdWordCountDocids(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();

            write_entries_into_database(
                merger,
                &index.field_id_word_count_docids,
                wtxn,
                deladd_serialize_add_side,
                merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap,
            )?;
            is_merged_database = true;
        }
        TypedChunk::WordDocids { .. } => {
            let span = tracing::trace_span!(target: "indexing::write_db", "word_docids");
            let _entered = span.enter();

            let mut word_docids_builder =
                MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            let mut exact_word_docids_builder =
                MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            let mut word_fid_docids_builder =
                MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            let mut fst_merger_builder = MergerBuilder::new(merge_ignore_values as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::WordDocids {
                    word_docids_reader,
                    exact_word_docids_reader,
                    word_fid_docids_reader,
                } = typed_chunk
                else {
                    unreachable!();
                };
                let clonable_word_docids = unsafe { as_cloneable_grenad(&word_docids_reader) }?;
                let clonable_exact_word_docids =
                    unsafe { as_cloneable_grenad(&exact_word_docids_reader) }?;

                word_docids_builder.push(word_docids_reader.into_cursor()?);
                exact_word_docids_builder.push(exact_word_docids_reader.into_cursor()?);
                word_fid_docids_builder.push(word_fid_docids_reader.into_cursor()?);
                fst_merger_builder.push(clonable_word_docids.into_cursor()?);
                fst_merger_builder.push(clonable_exact_word_docids.into_cursor()?);
            }

            let word_docids_merger = word_docids_builder.build();
            write_entries_into_database(
                word_docids_merger,
                &index.word_docids,
                wtxn,
                deladd_serialize_add_side,
                merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap,
            )?;

            let exact_word_docids_merger = exact_word_docids_builder.build();
            write_entries_into_database(
                exact_word_docids_merger,
                &index.exact_word_docids,
                wtxn,
                deladd_serialize_add_side,
                merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap,
            )?;

            let word_fid_docids_merger = word_fid_docids_builder.build();
            write_entries_into_database(
                word_fid_docids_merger,
                &index.word_fid_docids,
                wtxn,
                deladd_serialize_add_side,
                merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap,
            )?;

            // create fst from word docids
            let fst_merger = fst_merger_builder.build();
            let fst = merge_word_docids_reader_into_fst(fst_merger)?;
            let db_fst = index.words_fst(wtxn)?;

            // merge new fst with database fst
            let union_stream = fst.op().add(db_fst.stream()).union();
            let mut builder = fst::SetBuilder::memory();
            builder.extend_stream(union_stream)?;
            let fst = builder.into_set();
            index.put_words_fst(wtxn, &fst)?;
            is_merged_database = true;
        }
        TypedChunk::WordPositionDocids(_) => {
            let span = tracing::trace_span!(target: "indexing::write_db", "word_position_docids");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::WordPositionDocids(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();

            write_entries_into_database(
                merger,
                &index.word_position_docids,
                wtxn,
                deladd_serialize_add_side,
                merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap,
            )?;
            is_merged_database = true;
        }
        TypedChunk::FieldIdFacetNumberDocids(_) => {
            let span =
                tracing::trace_span!(target: "indexing::write_db","field_id_facet_number_docids");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            let mut data_size = 0;
            for typed_chunk in typed_chunks {
                let TypedChunk::FieldIdFacetNumberDocids(facet_id_number_docids) = typed_chunk
                else {
                    unreachable!();
                };

                data_size += facet_id_number_docids.len();
                builder.push(facet_id_number_docids.into_cursor()?);
            }
            let merger = builder.build();

            let indexer = FacetsUpdate::new(index, FacetType::Number, merger, None, data_size);
            indexer.execute(wtxn)?;
            is_merged_database = true;
        }
        TypedChunk::FieldIdFacetStringDocids(_) => {
            let span =
                tracing::trace_span!(target: "indexing::write_db", "field_id_facet_string_docids");
            let _entered = span.enter();

            let mut facet_id_string_builder =
                MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            let mut normalized_facet_id_string_builder =
                MergerBuilder::new(merge_deladd_btreeset_string as MergeFn);
            let mut data_size = 0;
            for typed_chunk in typed_chunks {
                let TypedChunk::FieldIdFacetStringDocids((
                    facet_id_string_docids,
                    normalized_facet_id_string_docids,
                )) = typed_chunk
                else {
                    unreachable!();
                };

                data_size += facet_id_string_docids.len();
                facet_id_string_builder.push(facet_id_string_docids.into_cursor()?);
                normalized_facet_id_string_builder
                    .push(normalized_facet_id_string_docids.into_cursor()?);
            }
            let facet_id_string_merger = facet_id_string_builder.build();
            let normalized_facet_id_string_merger = normalized_facet_id_string_builder.build();

            let indexer = FacetsUpdate::new(
                index,
                FacetType::String,
                facet_id_string_merger,
                Some(normalized_facet_id_string_merger),
                data_size,
            );
            indexer.execute(wtxn)?;
            is_merged_database = true;
        }
        TypedChunk::FieldIdFacetExistsDocids(_) => {
            let span =
                tracing::trace_span!(target: "indexing::write_db", "field_id_facet_exists_docids");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::FieldIdFacetExistsDocids(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();

            write_entries_into_database(
                merger,
                &index.facet_id_exists_docids,
                wtxn,
                deladd_serialize_add_side,
                merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap,
            )?;
            is_merged_database = true;
        }
        TypedChunk::FieldIdFacetIsNullDocids(_) => {
            let span =
                tracing::trace_span!(target: "indexing::write_db", "field_id_facet_is_null_docids");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::FieldIdFacetIsNullDocids(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();

            write_entries_into_database(
                merger,
                &index.facet_id_is_null_docids,
                wtxn,
                deladd_serialize_add_side,
                merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap,
            )?;
            is_merged_database = true;
        }
        TypedChunk::FieldIdFacetIsEmptyDocids(_) => {
            let span = tracing::trace_span!(target: "indexing::write_db", "field_id_facet_is_empty_docids");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::FieldIdFacetIsEmptyDocids(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();

            write_entries_into_database(
                merger,
                &index.facet_id_is_empty_docids,
                wtxn,
                deladd_serialize_add_side,
                merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap,
            )?;
            is_merged_database = true;
        }
        TypedChunk::WordPairProximityDocids(_) => {
            let span =
                tracing::trace_span!(target: "indexing::write_db", "word_pair_proximity_docids");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(merge_deladd_cbo_roaring_bitmaps as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::WordPairProximityDocids(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();

            write_entries_into_database(
                merger,
                &index.word_pair_proximity_docids,
                wtxn,
                deladd_serialize_add_side,
                merge_deladd_cbo_roaring_bitmaps_into_cbo_roaring_bitmap,
            )?;
            is_merged_database = true;
        }
        TypedChunk::FieldIdDocidFacetNumbers(_) => {
            let span =
                tracing::trace_span!(target: "indexing::write_db", "field_id_docid_facet_numbers");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(keep_first as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::FieldIdDocidFacetNumbers(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();

            let index_fid_docid_facet_numbers =
                index.field_id_docid_facet_f64s.remap_types::<Bytes, Bytes>();
            let mut iter = merger.into_stream_merger_iter()?;
            while let Some((key, value)) = iter.next()? {
                let reader = KvReaderDelAdd::new(value);
                if valid_lmdb_key(key) {
                    match (reader.get(DelAdd::Deletion), reader.get(DelAdd::Addition)) {
                        (None, None) => {}
                        (None, Some(new)) => index_fid_docid_facet_numbers.put(wtxn, key, new)?,
                        (Some(_), None) => {
                            index_fid_docid_facet_numbers.delete(wtxn, key)?;
                        }
                        (Some(_), Some(new)) => {
                            index_fid_docid_facet_numbers.put(wtxn, key, new)?
                        }
                    }
                }
            }
        }
        TypedChunk::FieldIdDocidFacetStrings(_) => {
            let span =
                tracing::trace_span!(target: "indexing::write_db", "field_id_docid_facet_strings");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(keep_first as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::FieldIdDocidFacetStrings(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();

            let index_fid_docid_facet_strings =
                index.field_id_docid_facet_strings.remap_types::<Bytes, Bytes>();
            let mut iter = merger.into_stream_merger_iter()?;
            while let Some((key, value)) = iter.next()? {
                let reader = KvReaderDelAdd::new(value);
                if valid_lmdb_key(key) {
                    match (reader.get(DelAdd::Deletion), reader.get(DelAdd::Addition)) {
                        (None, None) => {}
                        (None, Some(new)) => index_fid_docid_facet_strings.put(wtxn, key, new)?,
                        (Some(_), None) => {
                            index_fid_docid_facet_strings.delete(wtxn, key)?;
                        }
                        (Some(_), Some(new)) => {
                            index_fid_docid_facet_strings.put(wtxn, key, new)?
                        }
                    }
                }
            }
        }
        TypedChunk::GeoPoints(_) => {
            let span = tracing::trace_span!(target: "indexing::write_db", "geo_points");
            let _entered = span.enter();

            let mut builder = MergerBuilder::new(keep_first as MergeFn);
            for typed_chunk in typed_chunks {
                let TypedChunk::GeoPoints(chunk) = typed_chunk else {
                    unreachable!();
                };

                builder.push(chunk.into_cursor()?);
            }
            let merger = builder.build();

            let mut rtree = index.geo_rtree(wtxn)?.unwrap_or_default();
            let mut geo_faceted_docids = index.geo_faceted_documents_ids(wtxn)?;

            let mut iter = merger.into_stream_merger_iter()?;
            while let Some((key, value)) = iter.next()? {
                // convert the key back to a u32 (4 bytes)
                let docid = key.try_into().map(DocumentId::from_be_bytes).unwrap();

                let deladd_obkv = KvReaderDelAdd::new(value);
                if let Some(value) = deladd_obkv.get(DelAdd::Deletion) {
                    let geopoint = extract_geo_point(value, docid);
                    rtree.remove(&geopoint);
                    geo_faceted_docids.remove(docid);
                }
                if let Some(value) = deladd_obkv.get(DelAdd::Addition) {
                    let geopoint = extract_geo_point(value, docid);
                    rtree.insert(geopoint);
                    geo_faceted_docids.insert(docid);
                }
            }
            index.put_geo_rtree(wtxn, &rtree)?;
            index.put_geo_faceted_documents_ids(wtxn, &geo_faceted_docids)?;
        }
        TypedChunk::VectorPoints { .. } => {
            let span = tracing::trace_span!(target: "indexing::write_db", "vector_points");
            let _entered = span.enter();

            let mut remove_vectors_builder = MergerBuilder::new(keep_first as MergeFn);
            let mut manual_vectors_builder = MergerBuilder::new(keep_first as MergeFn);
            let mut embeddings_builder = MergerBuilder::new(keep_first as MergeFn);
            let mut params = None;
            for typed_chunk in typed_chunks {
                let TypedChunk::VectorPoints {
                    remove_vectors,
                    manual_vectors,
                    embeddings,
                    expected_dimension,
                    embedder_name,
                } = typed_chunk
                else {
                    unreachable!();
                };

                params = Some((expected_dimension, embedder_name));

                remove_vectors_builder.push(remove_vectors.into_cursor()?);
                manual_vectors_builder.push(manual_vectors.into_cursor()?);
                if let Some(embeddings) = embeddings {
                    embeddings_builder.push(embeddings.into_cursor()?);
                }
            }

            // typed chunks has always at least 1 chunk.
            let Some((expected_dimension, embedder_name)) = params else { unreachable!() };

            let embedder_index = index.embedder_category_id.get(wtxn, &embedder_name)?.ok_or(
                InternalError::DatabaseMissingEntry { db_name: "embedder_category_id", key: None },
            )?;
            let writer_index = (embedder_index as u16) << 8;
            // FIXME: allow customizing distance
            let writers: std::result::Result<Vec<_>, _> = (0..=u8::MAX)
                .map(|k| {
                    arroy::Writer::new(
                        index.vector_arroy,
                        writer_index | (k as u16),
                        expected_dimension,
                    )
                })
                .collect();
            let writers = writers?;

            // remove vectors for docids we want them removed
            let merger = remove_vectors_builder.build();
            let mut iter = merger.into_stream_merger_iter()?;
            while let Some((key, _)) = iter.next()? {
                let docid = key.try_into().map(DocumentId::from_be_bytes).unwrap();

                for writer in &writers {
                    // Uses invariant: vectors are packed in the first writers.
                    if !writer.del_item(wtxn, docid)? {
                        break;
                    }
                }
            }

            // add generated embeddings
            let merger = embeddings_builder.build();
            let mut iter = merger.into_stream_merger_iter()?;
            while let Some((key, value)) = iter.next()? {
                let docid = key.try_into().map(DocumentId::from_be_bytes).unwrap();
                let data = pod_collect_to_vec(value);
                // it is a code error to have embeddings and not expected_dimension
                let embeddings = crate::vector::Embeddings::from_inner(data, expected_dimension)
                    // code error if we somehow got the wrong dimension
                    .unwrap();

                if embeddings.embedding_count() > usize::from(u8::MAX) {
                    let external_docid = if let Ok(Some(Ok(index))) = index
                        .external_id_of(wtxn, std::iter::once(docid))
                        .map(|it| it.into_iter().next())
                    {
                        index
                    } else {
                        format!("internal docid={docid}")
                    };
                    return Err(crate::Error::UserError(crate::UserError::TooManyVectors(
                        external_docid,
                        embeddings.embedding_count(),
                    )));
                }
                for (embedding, writer) in embeddings.iter().zip(&writers) {
                    writer.add_item(wtxn, docid, embedding)?;
                }
            }

            // perform the manual diff
            let merger = manual_vectors_builder.build();
            let mut iter = merger.into_stream_merger_iter()?;
            while let Some((key, value)) = iter.next()? {
                // convert the key back to a u32 (4 bytes)
                let (left, _index) = try_split_array_at(key).unwrap();
                let docid = DocumentId::from_be_bytes(left);

                let vector_deladd_obkv = KvReaderDelAdd::new(value);
                if let Some(value) = vector_deladd_obkv.get(DelAdd::Deletion) {
                    let vector: Vec<f32> = pod_collect_to_vec(value);

                    let mut deleted_index = None;
                    for (index, writer) in writers.iter().enumerate() {
                        let Some(candidate) = writer.item_vector(wtxn, docid)? else {
                            // uses invariant: vectors are packed in the first writers.
                            break;
                        };
                        if candidate == vector {
                            writer.del_item(wtxn, docid)?;
                            deleted_index = Some(index);
                        }
                    }

                    // 🥲 enforce invariant: vectors are packed in the first writers.
                    if let Some(deleted_index) = deleted_index {
                        let mut last_index_with_a_vector = None;
                        for (index, writer) in writers.iter().enumerate().skip(deleted_index) {
                            let Some(candidate) = writer.item_vector(wtxn, docid)? else {
                                break;
                            };
                            last_index_with_a_vector = Some((index, candidate));
                        }
                        if let Some((last_index, vector)) = last_index_with_a_vector {
                            // unwrap: computed the index from the list of writers
                            let writer = writers.get(last_index).unwrap();
                            writer.del_item(wtxn, docid)?;
                            writers.get(deleted_index).unwrap().add_item(wtxn, docid, &vector)?;
                        }
                    }
                }

                if let Some(value) = vector_deladd_obkv.get(DelAdd::Addition) {
                    let vector = pod_collect_to_vec(value);

                    // overflow was detected during vector extraction.
                    for writer in &writers {
                        if !writer.contains_item(wtxn, docid)? {
                            writer.add_item(wtxn, docid, &vector)?;
                            break;
                        }
                    }
                }
            }

            tracing::debug!("Finished vector chunk for {}", embedder_name);
        }
        TypedChunk::ScriptLanguageDocids(_) => {
            let span = tracing::trace_span!(target: "indexing::write_db", "script_language_docids");
            let _entered = span.enter();

            for typed_chunk in typed_chunks {
                let TypedChunk::ScriptLanguageDocids(sl_map) = typed_chunk else { unreachable!() };
                for (key, (deletion, addition)) in sl_map {
                    let mut db_key_exists = false;
                    let final_value = match index.script_language_docids.get(wtxn, &key)? {
                        Some(db_values) => {
                            db_key_exists = true;
                            (db_values - deletion) | addition
                        }
                        None => addition,
                    };

                    if final_value.is_empty() {
                        // If the database entry exists, delete it.
                        if db_key_exists {
                            index.script_language_docids.delete(wtxn, &key)?;
                        }
                    } else {
                        index.script_language_docids.put(wtxn, &key, &final_value)?;
                    }
                }
            }
        }
    }

    Ok((RoaringBitmap::new(), is_merged_database))
}

/// Converts the latitude and longitude back to an xyz GeoPoint.
fn extract_geo_point(value: &[u8], docid: DocumentId) -> GeoPoint {
    let (lat, tail) = helpers::try_split_array_at::<u8, 8>(value).unwrap();
    let (lng, _) = helpers::try_split_array_at::<u8, 8>(tail).unwrap();
    let point = [f64::from_ne_bytes(lat), f64::from_ne_bytes(lng)];
    let xyz_point = lat_lng_to_xyz(&point);
    GeoPoint::new(xyz_point, (docid, point))
}

fn merge_word_docids_reader_into_fst(
    merger: Merger<CursorClonableMmap, MergeFn>,
) -> Result<fst::Set<Vec<u8>>> {
    let mut iter = merger.into_stream_merger_iter()?;
    let mut builder = fst::SetBuilder::memory();

    while let Some((k, _)) = iter.next()? {
        builder.insert(k)?;
    }

    Ok(builder.into_set())
}

/// Write provided entries in database using serialize_value function.
/// merge_values function is used if an entry already exist in the database.
#[tracing::instrument(level = "trace", skip_all, target = "indexing::write_db")]
fn write_entries_into_database<R, K, V, FS, FM>(
    merger: Merger<R, MergeFn>,
    database: &heed::Database<K, V>,
    wtxn: &mut RwTxn,
    serialize_value: FS,
    merge_values: FM,
) -> Result<()>
where
    R: io::Read + io::Seek,
    FS: for<'a> Fn(&'a [u8], &'a mut Vec<u8>) -> Result<&'a [u8]>,
    FM: for<'a> Fn(&[u8], &[u8], &'a mut Vec<u8>) -> Result<Option<&'a [u8]>>,
{
    puffin::profile_function!();
    let mut buffer = Vec::new();
    let database = database.remap_types::<Bytes, Bytes>();

    let mut iter = merger.into_stream_merger_iter()?;
    while let Some((key, value)) = iter.next()? {
        if valid_lmdb_key(key) {
            buffer.clear();
            let value = match database.get(wtxn, key)? {
                Some(prev_value) => merge_values(value, prev_value, &mut buffer)?,
                None => Some(serialize_value(value, &mut buffer)?),
            };
            match value {
                Some(value) => database.put(wtxn, key, value)?,
                None => {
                    database.delete(wtxn, key)?;
                }
            }
        }
    }
    Ok(())
}
