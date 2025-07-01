import hdbscan
import numpy as np
from typing import Dict, List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)


class ClusteringService:
    def __init__(self, min_cluster_size: int = 2, min_samples: int = 1):
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples
        
    def cluster_articles(self, embeddings: np.ndarray) -> Dict[int, int]:
        if len(embeddings) == 0:
            return {}
            
        logger.info(f"Clustering {len(embeddings)} articles")
        
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=self.min_cluster_size,
            min_samples=self.min_samples,
            metric='euclidean',
            cluster_selection_method='eom'
        )
        
        cluster_labels = clusterer.fit_predict(embeddings)
        
        doc_to_cluster = {i: label for i, label in enumerate(cluster_labels)}
        
        unique_clusters = set(cluster_labels) - {-1}
        logger.info(f"Found {len(unique_clusters)} clusters (excluding noise)")
        
        return doc_to_cluster
    
    def select_representative_articles(
        self, 
        embeddings: np.ndarray, 
        doc_to_cluster: Dict[int, int],
        n_representatives: int = 3
    ) -> Dict[int, List[int]]:
        cluster_representatives = {}
        
        unique_clusters = set(doc_to_cluster.values()) - {-1}
        
        for cluster_id in unique_clusters:
            cluster_indices = [
                doc_id for doc_id, cid in doc_to_cluster.items() 
                if cid == cluster_id
            ]
            
            if not cluster_indices:
                continue
                
            cluster_embeddings = embeddings[cluster_indices]
            
            cluster_centroid = np.mean(cluster_embeddings, axis=0)
            
            similarities = cosine_similarity(
                cluster_embeddings, 
                cluster_centroid.reshape(1, -1)
            ).flatten()
            
            n_reps = min(n_representatives, len(cluster_indices))
            top_indices = np.argsort(similarities)[-n_reps:][::-1]
            
            cluster_representatives[cluster_id] = [
                cluster_indices[idx] for idx in top_indices
            ]
            
        return cluster_representatives