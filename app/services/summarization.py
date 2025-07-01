import openai
from typing import List, Tuple
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class SummarizationService:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.api_key
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_cluster_summary(
        self, 
        articles: List[str], 
        max_articles: int = 3
    ) -> Tuple[str, str]:
        
        articles_to_summarize = articles[:max_articles]
        
        articles_text = "\n\n".join([
            f"기사 {i+1}:\n{article}" 
            for i, article in enumerate(articles_to_summarize)
        ])
        
        prompt = f"""다음 뉴스 기사들을 바탕으로 공통 주제를 파악하고, 간결한 제목과 요약을 만들어주세요.

{articles_text}

출력 형식:
제목: [15자 이내의 간결한 제목]
요약: [50자 이내로 이 기사들의 공통 주제와 핵심 내용을 설명]"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 뉴스 기사를 요약하는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            result = response.choices[0].message.content.strip()
            
            lines = result.split('\n')
            title = ""
            summary = ""
            
            for line in lines:
                if line.startswith("제목:"):
                    title = line.replace("제목:", "").strip()
                elif line.startswith("요약:"):
                    summary = line.replace("요약:", "").strip()
            
            if not title or not summary:
                title = "주제 클러스터"
                summary = "관련 기사들의 모음"
                
            logger.info(f"Generated title: {title}, summary: {summary}")
            return title, summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "주제 클러스터", "관련 기사들의 모음"