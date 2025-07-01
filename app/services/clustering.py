import hdbscan
import numpy as np
from typing import Dict, List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import logging

logger = logging.getLogger(__name__)


class ClusteringService:
    def __init__(self, min_cluster_size: int = 2, min_samples: int = 1, metric: str = 'cosine'):
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples
        self.metric = metric
        
    def cluster_articles(self, embeddings: np.ndarray) -> Dict[int, int]:
        if len(embeddings) == 0:
            return {}
            
        logger.info(f"Clustering {len(embeddings)} articles")
        
        # cosine 유사도를 사용하기 위해 임베딩을 정규화
        if self.metric == 'cosine':
            embeddings_normalized = normalize(embeddings, norm='l2')
            metric_to_use = 'euclidean'  # 정규화된 벡터의 euclidean distance는 cosine distance와 동일
        else:
            embeddings_normalized = embeddings
            metric_to_use = self.metric
        
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=self.min_cluster_size,
            min_samples=self.min_samples,
            metric=metric_to_use,
            cluster_selection_method='eom',
            cluster_selection_epsilon=0.15,  # 적절한 epsilon으로 균형잡힌 클러스터링
            alpha=1.2,  # 적절한 alpha로 균형잡힌 클러스터링
            prediction_data=True
        )
        
        cluster_labels = clusterer.fit_predict(embeddings_normalized)
        
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