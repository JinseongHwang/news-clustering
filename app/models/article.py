from pydantic import BaseModel
from typing import List, Optional


class Article(BaseModel):
    id: str
    content: str


class ArticleCluster(BaseModel):
    cluster_id: int
    articles: List[str]
    topic_title: str
    topic_summary: str
    

class ClusteringRequest(BaseModel):
    articles: List[Article]
    

class ClusteringResponse(BaseModel):
    clusters: List[ArticleCluster]