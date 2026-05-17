import streamlit as st
import google.generativeai as genai
import random

# 🔑 1. 구글 Gemini API 키 설정 및 절대경로 모델명 적용
GOOGLE_API_KEY = "AIzaSyAJtkCFGQGSjKtFejms06wCPRKHcn6IhAw"
genai.configure(api_key=GOOGLE_API_KEY)
# 구글 서버가 절대 헷갈리지 않도록 공식 전체 경로명으로 지정합니다.
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.set_page_config(page_title="⚡ 민주주의 런 AI 판정관", layout="centered")
st.title("⚡ 민주주의 런 : AI 미디어 판정관")
st.caption("6학년 사회 '민주주의와 미디어' 실시간 AI 팩트체크 센터")

# 시스템 초기화
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "auth_stage2" not in st.session_state:
    st.session_state.auth_stage2 = False
if "auth_stage4" not in st.session_state:
    st.session_state.auth_stage4 = False

# 👤 사용자 정보 입력
col1, col2 = st.columns(2)
with col1:
    user_name = st.text_input("👤 이름 입력", placeholder="홍길동")
with col2:
    user_team = st.selectbox("👥 소속 모둠 선택", [f"{i}조" for i in range(1, 7)])

# 🎚️ 단계 선택 라디오
choice_stage = st.radio("🎚️ 수행할 미션 단계를 선택하세요", ["1단계: 육하원칙 5줄 뉴스 기사", "2단계: 1줄 정책 제안서", "4단계: 독재 저항 반박 댓글"])

# 프롬프트 베이스 정의 (선생님의 무결점 지시문 내장)
base_prompt = """
너는 초등학교 6학년 사회 수업 '민주주의와 미디어' 게임의 엄격하고 공정한 'AI 국가정부 및 수석 편집장'이다.
[원칙] "오늘 점심 맛있었음", "학교 가기 싫음", "엄마가 밥 차려줌" 같은 장난성 글, 개인적인 일기장 같은 글, 사회 문제와 상관없는 소소한 글, 마침표 연타(....)나 자음 연타(ㅋㅋㅋ)는 내용이 아무리 길어도 무조건 [반려(실패)] 처리하고 단호하게 경고해야 한다.
결과와 피드백은 6학년 수준에 맞게 격려하면서도 엄격한 어조로, 3줄 이내로 짧고 명확하게 작성해라.
"""

# --- 1단계 인터페이스 ---
if choice_stage == "1단계: 육하원칙 5줄 뉴스 기사":
    st.subheader("📰 1단계: 육하원칙 5줄 뉴스 기사 작성")
    st.info("💡 사회 문제를 바탕으로 육하원칙 단서를 담아 엔터(줄바꿈)를 활용해 5줄 뉴스를 쓰세요.")
    text_s1 = st.text_area("뉴스 기사 입력창", placeholder="이곳에 기사를 작성하세요...")
    
    if st.button("뉴스 기사 발행하기 🚀"):
        if not user_name: 
            st.error("이름을 입력해 주세요!")
            st.stop()
        
        with st.spinner("AI 편집장이 팩트체크 중..."):
            prompt = f"{base_prompt}\n[미션] 학생들이 1단계 뉴스 기사를 제출했다. 내용: {text_s1}\n조건: 학교/사회 공공 문제를 다루고 육하원칙이 논리적으로 녹아있는가? 만족하면 '[1단계 통과] 축하합니다! 육하원칙과 사회적 팩트가 살아있는 훌륭한 뉴스 기사입니다. 전광판 업로드를 승인합니다! 교사에게 확인받고 2단계 암호를 받으세요.'라고 출력하고, 미달하면 '[1단계 반려(실패)]'와 누락된 이유를 친절히 말해줘."
            response = model.generate_content(prompt)
            st.write("---")
            if "통과" in response.text:
                st.success(response.text)
            else:
                st.error(response.text)

# --- 2단계 인터페이스 (🔑 암호 잠금: 2026 적용) ---
elif choice_stage == "2단계: 1줄 정책 제안서":
    st.subheader("🏛️ 2단계: 1줄 정책 제안서 제출")
    
    if not st.session_state.auth_stage2:
        code_s2 = st.text_input("🔒 2단계 비밀 코드를 입력하세요", type="password")
        if st.button("잠금 해제 🔓"):
            if code_s2 == "2026":
                st.session_state.auth_stage2 = True
                st.rerun()
            else: 
                st.error("비밀 코드가 올바르지 않습니다.")
            
    if st.session_state.auth_stage2:
        st.success("🔓 2단계 잠금이 해제되었습니다!")
        text_s2 = st.text_input("1줄 정책 제안 입력창", placeholder="문제를 해결할 구체적인 정책 대안을 제안하세요.")
        
        if st.button("정책 제안서 등록하기 🚀"):
            with st.spinner("AI 정부가 정책 심사 중..."):
                prompt = f"{base_prompt}\n[미션] 학생들이 2단계 1줄 정책 제안서를 제출했다. 내용: {text_s2}\n[엄격하고 공정한 채점 규칙]: 실행할 주체(누가)와 구체적인 해결 방법(규칙, 제도, 설치, 대책 등)이 논리적으로 모두 완벽하게 연결되었을 때만 '감점: -0점'을 주어라. 단순히 단어만 나열했거나, 구체적인 방법이 생략되었거나, 실천 불가능한 터무니없는 대안이라면 미흡한 정도에 따라 칼같이 1점부터 5점까지 감점해라. 출력 형식은 반드시 첫 줄에 '[2단계 판정 완료] 감점: -X점' 형태로만 시작하고 그 아래에 깎인 이유 또는 칭찬 피드백을 짧게 한 줄 적어줘."
                response = model.generate_content(prompt)
                st.write("---")
                st.info(response.text)

# --- 4단계 인터페이스 (🔑 암호 잠금: 0604 적용) ---
elif choice_stage == "4단계: 독재 저항 반박 댓글":
    st.subheader("🔥 4단계: 독재 저항 팩트체크 및 반박 댓글")
    
    if not st.session_state.auth_stage4:
        code_s4 = st.text_input("🔒 4단계 비밀 코드를 입력하세요", type="password")
        if st.button("잠금 해제 🔓"):
            if code_s4 == "0604":
                st.session_state.auth_stage4 = True
                st.rerun()
            else: 
                st.error("비밀 코드가 올바르지 않습니다.")
            
    if st.session_state.auth_stage4:
        st.success("🔓 4단계 잠금이 해제되었습니다!")
        text_s4 = st.text_area("반박 댓글 입력창", placeholder="정부의 가짜뉴스 선동에 맞서 논리적인 반박 댓글을 다세요.")
        
        if st.button("반박 댓글 송신 🚀"):
            with st.spinner("보안 네트워크로 송신 중..."):
                prompt = f"{base_prompt}\n[미션] 학생들이 4단계 독재 저항 댓글을 제출했다. 내용: {text_s4}\n[엄격하고 공정한 채점 규칙]: 감정적인 단순 비난이나 욕설은 논리 부족으로 간주하여 3~5점을 대폭 감점해라. '가짜뉴스 반박', '시민의 자유와 권리', '정확한 근거 요구' 등 민주주의 가치를 담은 타당한 근거가 조리 있게 작성되었을 때만 '감점: -0점'을 주어라. 출력 형식은 반드시 첫 줄에 '[4단계 판정 완료] 감점: -X점' 형태로만 시작하고 그 아래에 명확한 채점 이유를 적어줘."
                response = model.generate_content(prompt)
                st.write("---")
                st.warning(response.text)
