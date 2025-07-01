from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.model_name = model_name
        self.model = None
        
    def _load_model(self):
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Model loaded successfully")
    
    def embed_articles(self, articles: List[str]) -> np.ndarray:
        self._load_model()
        
        if not articles:
            return np.array([])
        
        logger.info(f"Embedding {len(articles)} articles")
        embeddings = self.model.encode(articles, convert_to_numpy=True)
        logger.info(f"Generated embeddings with shape: {embeddings.shape}")
        
        return embeddings