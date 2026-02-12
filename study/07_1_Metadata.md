# 메타데이터 (Metadata): 데이터에 붙은 꼬리표 🏷️

아키텍트님, `Document` 객체는 두 가지 정보를 담고 있습니다.

1.  **page_content**: 실제 내용물 ("대한민국의 수도는 서울...")
2.  **metadata**: 꼬리표 / 신상정보 (`{"source": "news.pdf", "page": 15}`)

---

## 1. 아키텍트의 시선: 영수증 vs 카드 명세서

*   **Content**: "15,000원" (금액 자체)
*   **Metadata**: "2024년 5월 1일", "스타벅스 강남점", "카드 번호 1234" (부가 정보)

만약 메타데이터가 없다면?
나중에 "이 15,000원이 어디서 쓴 거야?"라고 물었을 때 알 방법이 없습니다.

## 2. RAG에서의 역할 (Why use it?)

RAG 시스템에서 메타데이터는 **"근거(Citation)"**와 **"필터링(Filtering)"**에 쓰입니다.

### 📍 근거 표시 (Citation)
AI가 답변할 때 "이 정보는 **[회사내규.pdf 15페이지]**에서 가져왔습니다."라고 출처를 밝힐 수 있습니다.

### 🔍 필터링 (Filtering)
"2023년 뉴스 말고 **2024년 뉴스**에서만 찾아줘."
이런 고급 검색을 하려면 내용(Content)이 아니라 날짜(Metadata)를 봐야 합니다.

## 3. 코드 설계도

```python
from langchain.schema import Document

# 문서를 만들 때 꼬리표(metadata)를 같이 붙여줍니다.
doc = Document(
    page_content="서울의 인구는 약 940만 명입니다.",
    metadata={
        "source": "2024_통계청_보고서.pdf",
        "page": 3,
        "author": "김철수"
    }
)

# 나중에 꺼내볼 때
print(doc.page_content) # "서울의 인구는..."
print(doc.metadata["source"]) # "2024_통계청_보고서.pdf" (출처 확인!)
```

**결론:**
`create_documents`는 텍스트를 자르면서 자동으로 이런 `metadata` (예: 몇 번째 조각인지 등)를 관리하기 쉽게 객체로 감싸주는 역할을 합니다. 멍! 🐶
