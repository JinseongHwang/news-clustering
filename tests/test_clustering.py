import pytest
from app.models.article import Article
from app.services.embedding import EmbeddingService
from app.services.clustering import ClusteringService
import numpy as np


class TestEmbeddingService:
    def test_embed_articles(self):
        service = EmbeddingService()
        articles = [
            "This is the first article about technology",
            "This is the second article about technology",
            "This article is about sports"
        ]
        
        embeddings = service.embed_articles(articles)
        
        assert embeddings.shape[0] == 3
        assert embeddings.shape[1] == 384
        
    def test_embed_empty_articles(self):
        service = EmbeddingService()
        embeddings = service.embed_articles([])
        assert len(embeddings) == 0


class TestClusteringService:
    def test_cluster_articles(self):
        service = ClusteringService()
        
        embeddings = np.array([
            [0.1, 0.2, 0.3],
            [0.1, 0.2, 0.3],
            [0.9, 0.8, 0.7],
            [0.9, 0.8, 0.7]
        ])
        
        doc_to_cluster = service.cluster_articles(embeddings)
        
        assert len(doc_to_cluster) == 4
        
        unique_clusters = set(doc_to_cluster.values()) - {-1}
        assert len(unique_clusters) >= 1
        
    def test_select_representatives(self):
        service = ClusteringService()
        
        embeddings = np.array([
            [0.1, 0.2],
            [0.15, 0.25],
            [0.9, 0.8],
            [0.85, 0.75]
        ])
        
        doc_to_cluster = {0: 0, 1: 0, 2: 1, 3: 1}
        
        representatives = service.select_representative_articles(
            embeddings, doc_to_cluster, n_representatives=1
        )
        
        assert len(representatives) == 2
        assert all(len(reps) == 1 for reps in representatives.values())