# RAG (Retrieval-Augmented Generation): 지식 주입의 기술

## 1. 아키텍트의 시선: 오픈북 시험 (Open Book Exam)

LLM(건축가)은 똑똑하지만, **"최신 정보"**와 **"우리 회사 대외비"**는 모릅니다.
(학습 데이터가 2023년까지로 끊겨있기 때문입니다.)

이 문제를 해결하기 위해 **"교과서(Data)"**를 옆에 펴주고 시험을 보게 하는 기술,
그것이 바로 **RAG (검색 증강 생성)**입니다.

### 핵심 비유: 멍청한 도서관 사서

*   **LLM**: 책 내용을 읽고 요약해주는 똑똑한 **작가**.
*   **Vector DB**: 수만 권의 책이 꽂혀 있는 **도서관**.
*   **Retriever (검색기)**: 사용자의 질문을 듣고 관련 책을 찾아오는 **사서**.

**[작동 순서]**
1.  **사용자**: "우리 회사 복지 포인트 얼마야?"
2.  **사서(Retriever)**: (도서관을 뒤져서 '회사 내규.pdf' 15페이지를 찾아옴)
3.  **작가(LLM)**: (15페이지를 읽고) "내규에 따르면 연 100만 원입니다."

## 2. RAG의 5단계 파이프라인 (The Pipeline)

아키텍트는 이 5로공정을 설계해야 합니다.

1.  **Load (수집)**: PDF, Word, 웹사이트에서 글자를 긁어옵니다.
2.  **Split (청킹)**: 책 한 권을 통째로 주면 LLM이 체합니다. 문단 단위로 **잘게 쪼갭니다**.
3.  **Embed (임베딩)**: 쪼갠 글조각을 **숫자(벡터)**로 변환합니다. (컴퓨터가 이해하도록 번역)
4.  **Store (저장)**: 숫자로 변환된 데이터를 **벡터 DB(Vector DB)**에 저장합니다.
5.  **Retrieve (검색)**: 질문과 가장 비슷한 숫자 패턴을 가진 글조각을 꺼내옵니다.

## 3. 코드 설계도: 개념 잡기

실제 코드는 꽤 길지만, 흐름은 단순합니다.

```python
# 1. 문서 로드 (Load)
documents = load_pdf("company_rule.pdf")

# 2. 쪼개기 (Split)
chunks = split_text(documents, chunk_size=500)

# 3. 저장하기 (Embed & Store)
vector_db.add_documents(chunks)

# 4. 검색하기 (Retrieve)
# "복지 포인트"라고 물으면, 관련된 조각 3개를 찾아옴
relevant_docs = vector_db.similarity_search("복지 포인트")

# 5. 답변 생성 (Generate)
# 찾아온 조각(relevant_docs)을 참고해서 답하라고 시킴
llm.answer(question="복지 포인트 얼마?", context=relevant_docs)
```

## 4. 심화 질문

> **"그냥 PDF 파일 통째로 프롬프트에 붙여넣으면 안 되나요?"**
>
> *   **Context Window**: 파일이 너무 크면(예: 300페이지짜리 매뉴얼) 다 안 들어갑니다.
> *   **Cost**: 들어가더라도 돈(토큰 비용)이 엄청나게 깨집니다.
> *   **Accuracy**: 내용이 너무 많으면 LLM이 헷갈려서 오히려 엉뚱한 답을 합니다. (Lost in the Middle 현상)

## 5. 현실 점검 (Reality Check) 🚨

> "RAG가 만능인가요?"

*   **Garbage In, Garbage Out**: 원본 데이터(PDF)가 엉망이면(표가 깨지거나 오타가 많으면), 아무리 좋은 모델을 써도 답변은 쓰레기가 됩니다.
*   **데이터 전처리(Preprocessing)**가 RAG 성공의 80%를 좌우합니다.
