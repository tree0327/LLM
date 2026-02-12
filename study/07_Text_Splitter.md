# 데이터 나누기: 청킹 (Chunking)

아키텍트님, 정확합니다!
`chunk_size=500`은 **"약 500글자(또는 토큰) 단위로 자르겠다"**는 뜻입니다.

하지만 여기서 더 중요한 것은 **"어떻게 자르느냐(Overlap)"**입니다.

---

## 1. 아키텍트의 시선: 종이 찢기 vs 직소 퍼즐

### ❌ 잘못된 자르기 (No Overlap)
문서를 칼로 자르듯이 딱 500자에서 끊어버리면 어떻게 될까요?
하필 중요한 문장의 **허리가 잘릴 수 있습니다**.

> [조각 1] ...범인은 바로
> [조각 2] 홍길동입니다...

이렇게 되면 AI는 "범인이 누구야?"라는 질문에 대답을 못 합니다. 조각 1에는 이름이 없고, 조각 2에는 주어가 없으니까요.

### ✅ 올바른 자르기 (Overlap)
그래서 우리는 **"겹치게 자르기(Overlap)"**를 합니다.
`chunk_size=500`, `chunk_overlap=50`이라면?
앞 조각의 끝부분 50자를 뒤 조각의 시작부분에 **복사해서 붙여넣습니다**.

> [조각 1] ...범인은 바로 **홍길동입니다.**
> [조각 2] **범인은 바로 홍길동입니다.** 그는 어젯밤에...

이렇게 해야 문맥(Context)이 끊기지 않고 이어집니다. 마치 **직소 퍼즐의 튀어나온 부분**처럼요!

---

## 2. 코드 설계도: RecursiveCharacterTextSplitter

가장 많이 쓰는 도구입니다. 무식하게 글자 수로만 자르는 게 아니라, **문단(엔터) -> 문장(마침표) -> 단어(공백)** 순서로 예쁘게 자르려고 노력하는 녀석입니다.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. 텍스트 (예: 뉴스 기사)
text = "대한민국의 수도는 서울입니다. (아주 긴 텍스트라고 가정)..."

# 2. 자르는 칼 준비 (Splitter)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,    # 한 조각 크기 (약 500자)
    chunk_overlap=50   # 겹치는 구간 (50자)
)

# 3. 자르기
# create_documents를 쓰면 '글자'가 아니라 'Document 객체'로 만들어줍니다.
# (나중에 metadata를 넣기 위함입니다)
chunks = splitter.create_documents([text])

# 결과 확인
print(chunks[0].page_content) # 첫 번째 조각의 내용
print(chunks[1].page_content) # 두 번째 조각
```

## 3. 심화 질문

> **"Chunk Size는 무조건 작을수록 좋을까, 클수록 좋을까?"**
>
> *   **너무 작으면 (100자)**: 문맥을 파악하기 힘듭니다. (앞뒤 내용이 잘림)
> *   **너무 크면 (2000자)**: 검색(Retrieve)했을 때 쓸데없는 내용까지 다 딸려옵니다. (AI가 헷갈려 함)
> *   **정답**: 보통 **500~1000자** 사이가 국룰(Standard)입니다.
