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
        # 균형잡힌 클러스터링을 위한 파라미터 조정
        self.clustering_service = ClusteringService(
            min_cluster_size=2,  # 최소 클러스터 크기 유지
            min_samples=1,  # min_samples를 줄여서 더 많은 포인트를 클러스터에 포함
            metric='cosine'  # 코사인 유사도 사용
        )
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
        
        # 노이즈로 분류된 기사들도 개별 클러스터로 처리
        noise_articles = [i for i, cid in doc_to_cluster.items() if cid == -1]
        
        # 클러스터에 속한 기사들 처리
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
        
        # 노이즈 기사들을 개별 클러스터로 추가
        for idx, article_idx in enumerate(noise_articles):
            cluster_id = len(cluster_representatives) + idx
            article_id = article_ids[article_idx]
            article_content = article_contents[article_idx]
            
            title, summary = self.summarization_service.generate_cluster_summary(
                [article_content]
            )
            
            cluster = ArticleCluster(
                cluster_id=cluster_id,
                articles=[article_id],
                topic_title=title,
                topic_summary=summary
            )
            
            clusters.append(cluster)
        
        logger.info(f"Processed {len(articles)} articles into {len(clusters)} clusters")
        
        return clusters