# LangChain: AI 시스템의 조립 라인 🔗

## 1. 아키텍트의 시선: 왜 랭체인인가?

지금까지 우리는 **벽돌(LLM)**, **시멘트(Prompt)**, **철근(RAG)**을 각각 따로따로 배웠습니다.
하지만 건물을 지으려면 이 재료들을 **"하나로 연결"**해야 합니다.

그 역할을 하는 것이 **LangChain (랭체인)**입니다.
*   **역할**: "이거 하고, 그 다음에 저거 해." (순서 조율)
*   **비유**: **"컨베이어 벨트"** 또는 **"지하철 노선"** 🚇

## 2. 핵심 문법: LCEL (Pipe Syntax `|`)

랭체인의 꽃은 **`|` (파이프)** 연산자입니다.
유닉스(Unix)나 파이썬을 해보셨다면 익숙할 겁니다.
**"왼쪽의 결과물을 오른쪽으로 넘겨라"**는 뜻입니다.

> **`프롬프트 | 모델 | 출력파서`**

이 한 줄이 랭체인의 모든 것입니다.

### 🦁 비유: 지하철 노선도
1.  **출발역 (Prompt)**: 사용자 질문을 받아서 "요리법"으로 포장함.
2.  **환승역 (Model)**: 포장된 요리법을 요리사(AI)에게 줌.
3.  **도착역 (Output Parser)**: 요리사가 만든 음식을 예쁜 접시에 담음.

## 3. 코드 설계도: 기본 체인 만들기

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 1. 역(Station) 만들기
prompt = ChatPromptTemplate.from_template("너는 {topic} 전문가야. {question}에 대해 짧게 설명해.")
model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser() # 결과값(AI Message 객체)에서 글자(String)만 뽑아내는 기계

# 2. 선로 연결하기 (Chain)
chain = prompt | model | parser

# 3. 기차 출발 시키기 (Invoke)
result = chain.invoke({"topic": "양자역학", "question": "쉽게 알려줘"})

print(result)
# 결과: "양자역학은 아주 작은 입자들의 세계를 다루는..." (깔끔한 문자열)
```

## 4. 왜 편한가요?

그냥 코드로 짜면:
```python
# 귀찮은 방식
msg = prompt.format(topic="...", question="...")
res = model.predict(msg)
real_res = res.content
```
이렇게 3줄 써야 할 것을 `chain.invoke()` 한 방으로 끝낼 수 있습니다.
나중에 **RAG**나 **Memory**가 붙으면 이 체인이 10단계, 20단계로 길어지는데, 그때 `|` 문법이 빛을 발합니다.

---

이제 이 **체인**에 아까 배운 **RAG(Retriever)**를 끼워 넣으면 그게 바로 **"RAG Chain"**이 됩니다!
실습으로 넘어가볼까요? 멍! 🐶
