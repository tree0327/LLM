# 실습 11: RAG 전 과정 (단계별 정리) 🛠️

아키텍트님, 요청하신 대로 코드를 **7단계 공정**으로 깔끔하게 정리했습니다.
이 셀을 그대로 복사해서 실행해보세요.

---

## 0. 패키지 설치 (필수)
혹시 안 하셨다면 먼저 실행해주세요.
```bash
!pip install langchain langchain-openai langchain-chroma chromadb langchain-text-splitters
```

---

## 1. 라이브러리 임포트 (Import)
도구상자에서 필요한 도구들을 꺼냅니다.

```python
import os
from dotenv import load_dotenv

# 1. 문서 처리를 위한 도구
from langchain_core.documents import Document # (구버전 schema -> core.documents로 변경됨)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 2. AI 모델과 임베딩 도구
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# 3. 벡터 데이터베이스 도구
from langchain_chroma import Chroma
```

## 2. 환경 설정 (Setup)
금고를 열고 API 키를 준비합니다.

```python
load_dotenv()
# API 키가 잘 로드되었는지 확인 (보안상 앞 5자리만 출력)
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key Loaded: {api_key[:5]}...")
```

## 3. 데이터 준비 (Load)
실습용 가짜 데이터를 만듭니다. (나중엔 PDF Loader로 대체될 부분입니다)

```python
raw_text = """
[주식회사 사자개 사규]
제 1조 (목적) 본 규정은 사자개 주식회사의 복지를 규정한다.
제 2조 (근무시간) 근무시간은 오전 10시부터 오후 5시까지로 한다. (주 35시간)
제 3조 (복지 포인트) 전 직원은 매년 1월 1일, 복지 포인트 300만 원을 지급받는다.
제 4조 (휴가) 연차는 무제한으로 사용할 수 있다. 다만, 2주 이상 연속 사용 시 팀장 승인이 필요하다.
제 5조 (간식) 탕비실에는 항상 몬스터 에너지 드링크와 마카롱을 구비해야 한다.
"""
print("데이터 준비 완료.")
```

## 4. 텍스트 분할 (Split)
문서를 AI가 소화하기 좋게 잘게 쪼갭니다.

```python
# 100글자 단위로 자르고, 20글자씩 겹치게(Overlap) 설정
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

# 문자열을 'Document 객체'로 변환
chunks = splitter.create_documents([raw_text])

print(f"총 {len(chunks)}개의 조각(Chunk)이 생성되었습니다.")
print(f"첫 번째 조각 미리보기: {chunks[0].page_content}")
```

## 5. 임베딩 및 저장 (Embed & Store)
글자를 숫자로 바꿔서(Embedding) 도서관(DB)에 저장합니다.

```python
# Chroma DB를 메모리에 생성
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings() # 번역기 선택
)
print("데이터베이스 저장 완료.")
```

## 6. 질문 및 검색 (Retrieve)
사용자의 질문과 관련된 문서를 찾아옵니다.

```python
query = "회사 복지 포인트 얼마나 줘?"

# 유사도 검색 (상위 2개)
retrieved_docs = vector_db.similarity_search(query, k=2)

print(f"질문: {query}")
print("\n=== [검색된 컨닝 페이퍼] ===")
print(retrieved_docs[0].page_content)
```

## 7. 답변 생성 (Generate)
찾은 문서를 바탕으로 최종 답변을 생성합니다.

```python
# 모델 선택
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 프롬프트 조립 (RAG의 핵심!)
prompt = f"""
당신은 인사팀 AI 챗봇입니다.
아래의 [참고 문서]를 바탕으로 질문에 답하세요.

[참고 문서]
{retrieved_docs[0].page_content}

질문: {query}
"""

# 모델 호출
response = llm.invoke(prompt)

print("\n=== [AI 최종 답변] ===")
print(response.content)
```
