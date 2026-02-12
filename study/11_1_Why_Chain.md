# 왜 굳이 체인(Chain)을 써야 할까? (코드 비교) 🤔

아키텍트님, 갑자기 `|` 같은 기호가 나와서 당황하셨죠?
우리가 방금 짠 **RAG 코드**와 **체인 코드**를 나란히 놓고 비교해보면,
사실 **똑같은 일을 더 짧게 쓰는 방법**일 뿐이라는 걸 알 수 있습니다.

---

## 1. 우리가 방금 짠 코드 (Manual)

우리는 지금까지 이렇게 3단계로 코드를 짰습니다.

```python
# 1단계: 프롬프트 만들기 (f-string 사용)
prompt_text = f"질문: {query}에 대해 답해줘."

# 2단계: 모델 호출하기 (invoke)
response = llm.invoke(prompt_text)

# 3단계: 결과 꺼내기 (.content)
final_answer = response.content

print(final_answer)
```

이 코드는 아주 직관적이고 훌륭합니다.
하지만 매번 `response.content`라고 쓰는 게 조금 귀찮지 않나요?

## 2. 체인(Chain)을 쓴 코드 (Automatic)

랭체인은 위 3단계를 **부품(Component)**으로 만들어서 조립해버립니다.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 부품 1: 프롬프트 (f-string 대신 템플릿 사용)
prompt = ChatPromptTemplate.from_template("질문: {topic}에 대해 답해줘.")

# 부품 2: 모델 (우리가 쓰던 그 llm)
model = llm

# 부품 3: 파서 (새로운 친구!)
# 역할: response.content를 대신 꺼내주는 기계
output_parser = StrOutputParser()

# 조립! (1 -> 2 -> 3)
chain = prompt | model | output_parser

# 실행! (invoke 한 번으로 끝)
final_answer = chain.invoke({"topic": "양자역학"})
print(final_answer)
```

## 3. 무엇이 다른가요?

| 구분 | 수동 코드 (Manual) | 체인 코드 (Chain) |
| :--- | :--- | :--- |
| **프롬프트** | 파이썬 f-string (`f"..."`) | `ChatPromptTemplate` 객체 |
| **결과 추출** | `response.content` 직접 조회 | `StrOutputParser`가 자동 추출 |
| **연결 방식** | 변수에 담아서 넘겨줌 | `|` 기호로 연결 |

결국 **체인(Chain)**은 거창한 신기술이 아니라,
우리가 매번 하는 **[프롬프트 포장 -> 모델 호출 -> 글자 꺼내기]** 패턴을
**자동화**해주는 도구일 뿐입니다.

특히 **`StrOutputParser`**는 별거 아닙니다. 그냥 **`.content`를 대신 해주는 애**입니다.

이 관점으로 보면 아까 그 실습 코드가 좀 더 친숙하게 느껴지실 겁니다.
다시 한 번 천천히 실습 코드를 보시겠습니까? 멍! 🐶
