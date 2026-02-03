import streamlit as st
from audiorecorder import audiorecorder         # 브라우저에서 음성 녹음 위젯
from openai_service import stt, ask_gpt, tts    # openai_service 내 기능 모듈

def main():
    # 페이지 기본 설정
    st.set_page_config(
        page_title = 'Voice Chatbot',  # 브라우저 탭 제목
        page_icon = '🎤',             # 탭 아이콘
        layout = 'wide'                # 넓은 레이아웃 설정
    )
    st.header('🎤Voice Chatbot🎤')   # 상단 헤더
    st.markdown('---')                # 구분선

    # 처리 절차 설명 토글 UI
    with st.expander('Voice Chatbot 프로그램 처리절차', expanded=False):
        st.write(
            """
            1. 녹음하기 버튼을 눌러 질문을 녹음합니다.
            2. 녹음이 완료되면 자동으로 Whisper모델을 이용해 음성을 텍스트로 변환합니다. 
            3. 변환된 텍스트로 LLM에 질의후 응답을 받습니다.
            4. LLM의 응답을 다시 TTS모델을 사용해 음성으로 변환하고 이를 사용자에게 들려줍니다.
            5. 모든 질문/답변은 채팅형식의 텍스트로 제공합니다.
            """
        )
    
    system_prompt = '당신은 친절한 챗봇입니다. 사용자의 질문에 50단어 이내로 간결하게 답변해주세요.'
    if 'messages' not in st.session_state:  # 대화 히스토리가 없으면 초기화
        # 채팅 시작하는 system 메시지 설정
        st.session_state['messages'] = [{'role': 'system', 'content': system_prompt}]
    if 'check_reset' not in st.session_state:    # 초기화 버튼 클릭 여부 플래그가 없으면
        st.session_state['check_reset'] = False  # 기본값 False 로 설정
    
    # 사이드바 영역
    with st.sidebar:
        model = st.radio(label='GTP 모델', options=['gpt-4.1-mini', 'gpt-5-nano', 'gpt-5.2'], index=0)
        print(f'{model = }')  # 서버 콘솔에 모델 출력 (디버깅용)
    
        if st.button(label='초기화'):    # 초기화 버튼 클릭시
            # 대화 히스토리를 system 메시지로 리셋
            st.session_state['messages'] = [{'role': 'system', 'content': system_prompt}]
            st.session_state['check_reset'] = True  # 방금 리셋했음 표시(녹음 처리 방지)
    
    col1, col2 = st.columns(2)    # 화면단을 2열로 분할
    with col1:                    # 왼쪽 컬럼 (녹음/음성 처리)
        st.subheader('녹음하기')
        audio = audiorecorder()   # 브라우저에서 음성 녹음 위젯 렌더링

        # 녹음이 1초이상 있고, 리셋 직후가 아니면
        if (audio.duration_seconds > 0) and (not st.session_state['check_reset']):
            st.audio(audio.export().read())  # 녹음된 음성을 화면에서 재생 (바이너리 read)

            query: str = stt(audio)    # STT로 음성 -> 텍스트 변환
            print(f'{query = }')

            st.session_state['messages'].append({'role': 'user', 'content': query})  # 사용자 메시지를 히스토리에 추가
            response: str = ask_gpt(st.session_state['messages'], model)  # 선택 모델로 GPT 응답
            print(f'{response = }')
            st.session_state['messages'].append({'role': 'assistant', 'content': response})  # assistant 응답을 히스토리에 추가

            base64_encoded_audio : str = tts(response)  # TTS로 응답 텍스트 -> 음성(mp3) 생성 후 base64 문자열 반환
            st.html(f'''
                <audio autoplay='true'>
                    <source src='data:audio/mp3;base64,{base64_encoded_audio}'>
                </audio>
            ''')  # base64 데이터 URI형태로 브라우저에서 바로 재생
        else:  # 리셋 직후 1회 처리 방지 후 상태를 False로 변경
            st.session_state['check_reset'] = False
    
    with col2:    # 오른쪽 컬럼 (텍스트 채팅 로그)
        st.subheader('질문/답변')
        # 녹음이 1초이상 있고, 리셋 직후가 아니면
        if (audio.duration_seconds > 0) and (not st.session_state['check_reset']):
            for message in st.session_state['messages']:
                role = message['role']        # system/user/assistant
                content = message['content']  # 메시지 텍스트 추출

                if role == 'system':          # system 메시지는 화면 채팅에 출력하지 않음
                    continue
                
                with st.chat_message(role):  # role에 맞는 채팅 버블 UI 생성
                    st.markdown(content)     # 메시지 텍스트 출력

# 스크립트를 직접 실행할 때 main 실행
if __name__ == '__main__':
    main()