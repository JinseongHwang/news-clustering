# News Clustering API

뉴스 기사를 자동으로 군집화하고 요약하는 API 서비스입니다. 유사한 주제의 뉴스 기사들을 자동으로 그룹화하고, 각 그룹에 대한 대표 제목과 요약을 생성합니다.

## 주요 기능

- **다국어 기사 임베딩**: Sentence Transformers를 사용한 다국어 텍스트 벡터화
- **자동 군집화**: HDBSCAN 알고리즘으로 최적의 클러스터 수 자동 결정
- **대표 기사 선정**: 각 클러스터 중심에 가장 가까운 기사 선택
- **AI 요약 생성**: OpenAI GPT를 이용한 클러스터별 제목 및 요약 자동 생성

## 시스템 요구사항

- Python 3.8 이상
- 메모리: 최소 4GB (대량 기사 처리 시 8GB 권장)
- OpenAI API 키 (GPT 사용을 위해 필요)

## 설치 및 설정

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd news-clustering
```

### 2. 가상환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일을 열어 OpenAI API 키 입력
# OPENAI_API_KEY=your_actual_api_key_here
```

## 서버 실행

```bash
# 개발 서버 실행 (자동 리로드 활성화)
python run_server.py

# 또는 직접 uvicorn 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

## API 사용법

### 엔드포인트

- `POST /api/v1/cluster` - 뉴스 기사 군집화 및 요약

### 요청 예시

```bash
curl -X POST "http://localhost:8000/api/v1/cluster" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [
      {
        "id": "1", 
        "content": "트럼프는 취임식 연설에서 미국 우선주의를 강조했다. 그는 국내 산업 보호와 일자리 창출을 최우선 과제로 삼겠다고 밝혔다."
      },
      {
        "id": "2", 
        "content": "도널드 트럼프의 첫 연설, 전문가들은 경제 보호주의 강화로 해석한다. 무역 정책의 대대적인 변화가 예상된다."
      },
      {
        "id": "3",
        "content": "한국 축구대표팀이 월드컵 예선에서 승리했다. 손흥민의 활약이 돋보였다."
      }
    ]
  }'
```

### 응답 예시

```json
{
  "clusters": [
    {
      "cluster_id": 0,
      "articles": ["1", "2"],
      "topic_title": "트럼프 취임 연설",
      "topic_summary": "트럼프의 미국 우선주의 정책과 경제 보호주의 강화를 다룬 기사 클러스터"
    },
    {
      "cluster_id": 1,
      "articles": ["3"],
      "topic_title": "한국 축구 승리",
      "topic_summary": "월드컵 예선에서 한국 대표팀의 승리와 손흥민의 활약을 다룬 기사"
    }
  ]
}
```

## 프로젝트 구조

```
news-clustering/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 애플리케이션 진입점
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API 라우트 정의
│   ├── models/
│   │   ├── __init__.py
│   │   └── article.py       # Pydantic 모델 정의
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embedding.py     # 텍스트 임베딩 서비스
│   │   ├── clustering.py    # HDBSCAN 군집화 서비스
│   │   ├── summarization.py # GPT 요약 생성 서비스
│   │   └── news_clustering.py # 통합 뉴스 클러스터링 서비스
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── test_api.py          # API 엔드포인트 테스트
│   └── test_clustering.py   # 클러스터링 로직 테스트
├── requirements.txt         # Python 의존성
├── run_server.py           # 서버 실행 스크립트
├── .env.example            # 환경변수 예시
├── .gitignore
├── README.md               # 이 파일
├── CLAUDE.md               # Claude Code용 가이드
└── prd.md                  # 제품 요구사항 문서
```

## 테스트

```bash
# 전체 테스트 실행
pytest tests/

# 특정 테스트 파일 실행
pytest tests/test_clustering.py

# 상세 출력과 함께 실행
pytest -v tests/

# 테스트 커버리지 확인
pytest --cov=app tests/
```

## 성능 최적화

- **임베딩 캐싱**: 동일한 기사에 대한 반복적인 임베딩 계산 방지 (향후 구현 예정)
- **배치 처리**: 대량의 기사를 효율적으로 처리
- **GPU 지원**: CUDA가 있는 경우 자동으로 GPU 사용

## 제한사항

- 한 번에 최대 1,000개의 기사 처리 권장
- 각 기사는 최소 50자 이상이어야 정확한 클러스터링 가능
- OpenAI API 호출 비용 발생 (클러스터당 1회)

## 문제 해결

### 일반적인 문제

1. **ImportError**: 가상환경이 활성화되어 있는지 확인
2. **OpenAI API 오류**: `.env` 파일의 API 키가 올바른지 확인
3. **메모리 부족**: 처리할 기사 수를 줄이거나 시스템 메모리 증설

### 로그 확인

서버 실행 시 콘솔에 상세한 로그가 출력됩니다. 문제 발생 시 로그를 확인하세요.

## 기여 방법

1. 이 저장소를 포크합니다
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

**중요**: 코드 변경 시 반드시 README.md도 함께 업데이트해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.