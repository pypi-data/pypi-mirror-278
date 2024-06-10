use rayon::iter::{IntoParallelIterator as _, ParallelIterator as _};

use super::error::{EmbedError, EmbedErrorKind, NewEmbedderError, NewEmbedderErrorKind};
use super::rest::{Embedder as RestEmbedder, EmbedderOptions as RestEmbedderOptions};
use super::{DistributionShift, Embeddings};
use crate::error::FaultSource;
use crate::ThreadPoolNoAbort;

#[derive(Debug)]
pub struct Embedder {
    rest_embedder: RestEmbedder,
}

#[derive(Debug, Clone, Hash, PartialEq, Eq, serde::Deserialize, serde::Serialize)]
pub struct EmbedderOptions {
    pub embedding_model: String,
    pub url: Option<String>,
    pub api_key: Option<String>,
    pub distribution: Option<DistributionShift>,
}

impl EmbedderOptions {
    pub fn with_default_model(api_key: Option<String>, url: Option<String>) -> Self {
        Self { embedding_model: "nomic-embed-text".into(), api_key, url, distribution: None }
    }
}

impl Embedder {
    pub fn new(options: EmbedderOptions) -> Result<Self, NewEmbedderError> {
        let model = options.embedding_model.as_str();
        let rest_embedder = match RestEmbedder::new(RestEmbedderOptions {
            api_key: options.api_key,
            dimensions: None,
            distribution: options.distribution,
            url: options.url.unwrap_or_else(get_ollama_path),
            query: serde_json::json!({
                "model": model,
            }),
            input_field: vec!["prompt".to_owned()],
            path_to_embeddings: Default::default(),
            embedding_object: vec!["embedding".to_owned()],
            input_type: super::rest::InputType::Text,
        }) {
            Ok(embedder) => embedder,
            Err(NewEmbedderError {
                kind:
                    NewEmbedderErrorKind::CouldNotDetermineDimension(EmbedError {
                        kind: super::error::EmbedErrorKind::RestOtherStatusCode(404, error),
                        fault: _,
                    }),
                fault: _,
            }) => {
                return Err(NewEmbedderError::could_not_determine_dimension(
                    EmbedError::ollama_model_not_found(error),
                ))
            }
            Err(error) => return Err(error),
        };

        Ok(Self { rest_embedder })
    }

    pub fn embed(&self, texts: Vec<String>) -> Result<Vec<Embeddings<f32>>, EmbedError> {
        match self.rest_embedder.embed(texts) {
            Ok(embeddings) => Ok(embeddings),
            Err(EmbedError { kind: EmbedErrorKind::RestOtherStatusCode(404, error), fault: _ }) => {
                Err(EmbedError::ollama_model_not_found(error))
            }
            Err(error) => Err(error),
        }
    }

    pub fn embed_chunks(
        &self,
        text_chunks: Vec<Vec<String>>,
        threads: &ThreadPoolNoAbort,
    ) -> Result<Vec<Vec<Embeddings<f32>>>, EmbedError> {
        threads
            .install(move || {
                text_chunks.into_par_iter().map(move |chunk| self.embed(chunk)).collect()
            })
            .map_err(|error| EmbedError {
                kind: EmbedErrorKind::PanicInThreadPool(error),
                fault: FaultSource::Bug,
            })?
    }

    pub fn chunk_count_hint(&self) -> usize {
        self.rest_embedder.chunk_count_hint()
    }

    pub fn prompt_count_in_chunk_hint(&self) -> usize {
        self.rest_embedder.prompt_count_in_chunk_hint()
    }

    pub fn dimensions(&self) -> usize {
        self.rest_embedder.dimensions()
    }

    pub fn distribution(&self) -> Option<DistributionShift> {
        self.rest_embedder.distribution()
    }
}

fn get_ollama_path() -> String {
    // Important: Hostname not enough, has to be entire path to embeddings endpoint
    std::env::var("MEILI_OLLAMA_URL").unwrap_or("http://localhost:11434/api/embeddings".to_string())
}
