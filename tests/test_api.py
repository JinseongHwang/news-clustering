import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.article import Article


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_cluster_empty_articles():
    response = client.post("/api/v1/cluster", json={"articles": []})
    assert response.status_code == 400


def test_cluster_articles_mock():
    articles = [
        {"id": "1", "content": "트럼프는 취임식 연설에서 미국 우선주의를 강조했다."},
        {"id": "2", "content": "도널드 트럼프의 첫 연설, 전문가들은 경제 보호주의 강화로 해석한다."},
        {"id": "3", "content": "월드컵에서 한국 팀이 승리했다."}
    ]
    
    response = client.post("/api/v1/cluster", json={"articles": articles})
    
    assert response.status_code == 200
    
    data = response.json()
    assert "clusters" in data