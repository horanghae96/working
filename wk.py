import streamlit as st
from datetime import datetime

# 앱 제목
st.title("경력 계산기")

# 최대 경력 수 설정
MAX_EXPERIENCES = 5

# 세션 상태 초기화
if 'experiences' not in st.session_state:
    st.session_state.experiences = []
if 'current_experience_index' not in st.session_state:
    st.session_state.current_experience_index = 0
if 'is_input_finished' not in st.session_state:
    st.session_state.is_input_finished = False

# 경력 추가 버튼 클릭 후 폼
def add_experience(start_date, end_date):
    if start_date and end_date:
        st.session_state.experiences.append((start_date, end_date))
        st.session_state.current_experience_index += 1

# 입력 폼
if st.session_state.current_experience_index < MAX_EXPERIENCES:
    st.subheader(f"경력 {st.session_state.current_experience_index + 1}")

    # 근무 시작일 입력
    start_date = st.date_input("근무 시작일:", key=f'start_date_{st.session_state.current_experience_index}')

    # 근무 종료일 입력
    end_date = st.date_input("근무 종료일:", key=f'end_date_{st.session_state.current_experience_index}')

    # 추가 버튼
    if st.button("추가"):
        add_experience(start_date, end_date)
        st.success(f"경력 {st.session_state.current_experience_index}이 추가되었습니다.")

    # 다음 경력 추가 또는 입력 완료 버튼
    if st.session_state.current_experience_index < MAX_EXPERIENCES:
        next_action = st.selectbox("다음 행동을 선택하세요:", ["다음 경력 추가", "입력 완료"], key='next_action')

        if next_action == "입력 완료" and st.button("저장"):
            st.session_state.is_input_finished = True
            st.success("경력 입력이 완료되었습니다.")
else:
    st.session_state.is_input_finished = True

# 경력 요약 및 총 근무 기간 계산 및 표시
if st.session_state.is_input_finished:
    st.subheader("경력 요약")
    total_days = 0

    for idx, (start_date, end_date) in enumerate(st.session_state.experiences):
        # 근무 일수 계산
        days = (end_date - start_date).days
        total_days += days

        # 년, 월, 일 계산
        years, remainder = divmod(days, 365)  # 대략적인 연도 계산
        months, days = divmod(remainder, 30)  # 대략적인 월 계산

        st.write(f"경력 {idx + 1}: {years}년 {months}개월 {days}일 (시작: {start_date}, 종료: {end_date})")

    # 총 기간 계산
    total_years, total_remainder = divmod(total_days, 365)
    total_months, total_days = divmod(total_remainder, 30)

    # 총 경력 표시 (큰 글자)
    total_experience_display = f"총 근무 기간: {total_years}년 {total_months}개월 {total_days}일"
    st.markdown(f"<h2 style='color: blue;'>{total_experience_display}</h2>", unsafe_allow_html=True)

    # 새로 시작하기 버튼
    if st.button("새로운 경력 입력 시작"):
        st.session_state.experiences.clear()
        st.session_state.is_input_finished = False
        st.session_state.current_experience_index = 0
        st.success("새로운 경력 입력을 시작합니다.")