from fastapi import APIRouter, HTTPException
from app.models.article import ClusteringRequest, ClusteringResponse
from app.services.news_clustering import NewsClusteringService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
clustering_service = NewsClusteringService()


@router.post("/cluster", response_model=ClusteringResponse)
async def cluster_articles(request: ClusteringRequest):
    try:
        if not request.articles:
            raise HTTPException(status_code=400, detail="No articles provided")
        
        logger.info(f"Received clustering request with {len(request.articles)} articles")
        
        clusters = clustering_service.process_articles(request.articles)
        
        return ClusteringResponse(clusters=clusters)
        
    except Exception as e:
        logger.error(f"Error processing clustering request: {e}")
        raise HTTPException(status_code=500, detail=str(e))