from typing import List
import logging
from app.models.article import Article, ArticleCluster
from app.services.embedding import EmbeddingService
from app.services.clustering import ClusteringService
from app.services.summarization import SummarizationService

logger = logging.getLogger(__name__)


class NewsClusteringService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.clustering_service = ClusteringService()
        self.summarization_service = SummarizationService()
    
    def process_articles(self, articles: List[Article]) -> List[ArticleCluster]:
        if not articles:
            return []
        
        article_contents = [article.content for article in articles]
        article_ids = [article.id for article in articles]
        
        embeddings = self.embedding_service.embed_articles(article_contents)
        
        doc_to_cluster = self.clustering_service.cluster_articles(embeddings)
        
        cluster_representatives = self.clustering_service.select_representative_articles(
            embeddings, doc_to_cluster
        )
        
        clusters = []
        
        for cluster_id, representative_indices in cluster_representatives.items():
            cluster_article_indices = [
                i for i, cid in doc_to_cluster.items() 
                if cid == cluster_id
            ]
            
            cluster_article_ids = [article_ids[i] for i in cluster_article_indices]
            
            representative_contents = [
                article_contents[i] for i in representative_indices
            ]
            
            title, summary = self.summarization_service.generate_cluster_summary(
                representative_contents
            )
            
            cluster = ArticleCluster(
                cluster_id=cluster_id,
                articles=cluster_article_ids,
                topic_title=title,
                topic_summary=summary
            )
            
            clusters.append(cluster)
        
        logger.info(f"Processed {len(articles)} articles into {len(clusters)} clusters")
        
        return clusters