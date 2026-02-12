# 실습 12: LCEL 기초 (체인 만들기) 🔗

아키텍트님, RAG를 잠시 내려놓고 **"조립 라인(Chain)"**을 만드는 연습을 해봅시다.
이 `|` (파이프) 문법만 익히면, 나중에 RAG, 챗봇, 에이전트 다 만들 수 있습니다.

---

## 1. 라이브러리 임포트

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
```

## 2. 재료 준비 (역 3개 만들기)

기차역 3개를 미리 만들어둡니다.

```python
# 역 1: 프롬프트 (요리 주문서)
prompt = ChatPromptTemplate.from_template("너는 {topic} 전문가야. {question}에 대해 짧게 설명해.")

# 역 2: 모델 (요리사)
model = ChatOpenAI(model="gpt-4o-mini")

# 역 3: 파서 (웨이터)
# AI의 답변(객체)에서 순수한 글자(String)만 뽑아내는 도구
parser = StrOutputParser()
```

## 3. 체인 조립 (선로 연결)

### [실험 A] 파서 없이 연결하기
```python
chain_1 = prompt | model

result_1 = chain_1.invoke({"topic": "초콜릿", "question": "효능이 뭐야?"})
print(f"타입: {type(result_1)}")
print(result_1)
```
*   **결과**: `AIMessage(content='초콜릿은 스트레스를...')`
*   **문제**: 결과가 지저분한 '메시지 객체'로 나옵니다. 우리는 알맹이(`content`)만 필요한데 말이죠.

### [실험 B] 파서까지 연결하기 (완성형)
```python
# 파이프(|)로 3단 합체!
chain_2 = prompt | model | parser

result_2 = chain_2.invoke({"topic": "초콜릿", "question": "효능이 뭐야?"})
print(f"타입: {type(result_2)}")
print(result_2)
```
*   **결과**: `'초콜릿은 스트레스를...'`
*   **해설**: `StrOutputParser`가 중간에서 껍데기를 벗기고 **깔끔한 문자열**만 줬습니다.

---

## 🦁 아키텍트의 팁: LCEL이 뭔가요?
**L**ang**C**hain **E**xpression **L**anguage의 약자입니다.
복잡한 파이썬 코드 대신 **`|` 기호 하나로 과정을 연결**하는 랭체인만의 문법입니다.

> **"왼쪽에서 만든 걸, 오른쪽으로 넘겨라!"**

이것만 기억하시면 됩니다. 이번 실습이 끝나면 드디어 **[RAG + Chain]**을 합체시킬 수 있습니다! 멍! 🐶
