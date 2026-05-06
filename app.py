import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="K-Indie Film BEP Calculator",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 한국 독립영화 손익분기점 계산기")
st.write("제작비, 마케팅비, 배급비, 티켓 가격을 바탕으로 독립영화의 예상 손익분기 관객 수를 계산합니다.")

st.sidebar.header("📌 영화 정보 입력")

film_title = st.sidebar.text_input("영화 제목", "나의 독립영화")

production_budget = st.sidebar.number_input(
    "제작비 (원)", min_value=0, value=80000000, step=1000000
)

marketing_cost = st.sidebar.number_input(
    "마케팅비 (원)", min_value=0, value=15000000, step=1000000
)

distribution_fee = st.sidebar.number_input(
    "배급 수수료 / 배급비 (원)", min_value=0, value=10000000, step=1000000
)

other_costs = st.sidebar.number_input(
    "기타 비용 (원)", min_value=0, value=5000000, step=1000000
)

average_ticket_price = st.sidebar.number_input(
    "평균 티켓 가격 (원)", min_value=1000, value=11000, step=500
)

st.sidebar.header("💰 수익 배분율")

theater_share = st.sidebar.slider("극장 몫 (%)", 0, 100, 50)
distributor_share = st.sidebar.slider("배급사 몫 (%)", 0, 100, 10)
producer_share = st.sidebar.slider("제작/투자자 회수율 (%)", 0, 100, 40)

total_share = theater_share + distributor_share + producer_share

if total_share != 100:
    st.sidebar.warning(f"현재 총합은 {total_share}%입니다. 보통 100%가 되도록 조정하세요.")

total_cost = production_budget + marketing_cost + distribution_fee + other_costs

producer_revenue_per_ticket = average_ticket_price * (producer_share / 100)

if producer_revenue_per_ticket > 0:
    break_even_admissions = total_cost / producer_revenue_per_ticket
else:
    break_even_admissions = 0

break_even_gross_revenue = break_even_admissions * average_ticket_price

st.subheader(f"📽️ {film_title} 분석 결과")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "총비용",
    f"{total_cost:,.0f}원",
    help="제작비, 마케팅비, 배급비, 기타 비용을 모두 합친 금액입니다."
)

col2.metric(
    "관객 1명당 제작사 회수액",
    f"{producer_revenue_per_ticket:,.0f}원",
    help="티켓 가격 중 제작/투자자에게 돌아오는 예상 금액입니다."
)

col3.metric(
    "손익분기 관객 수",
    f"{break_even_admissions:,.0f}명",
    help="투입한 총비용을 회수하기 위해 필요한 최소 관객 수입니다."
)

col4.metric(
    "필요 총매출",
    f"{break_even_gross_revenue:,.0f}원",
    help="손익분기점에 도달하기 위해 극장에서 발생해야 하는 전체 매출입니다."
)

st.divider()

st.subheader("🎯 관객 수 시나리오 시뮬레이션")

pessimistic = st.number_input("비관적 관객 수", min_value=0, value=3000, step=1000)
realistic = st.number_input("현실적 관객 수", min_value=0, value=10000, step=1000)
optimistic = st.number_input("낙관적 관객 수", min_value=0, value=30000, step=1000)

scenario_data = pd.DataFrame({
    "시나리오": ["비관적", "현실적", "낙관적"],
    "관객 수": [pessimistic, realistic, optimistic]
})

scenario_data["총매출"] = scenario_data["관객 수"] * average_ticket_price
scenario_data["제작사 회수액"] = scenario_data["관객 수"] * producer_revenue_per_ticket
scenario_data["손익"] = scenario_data["제작사 회수액"] - total_cost

st.dataframe(scenario_data, use_container_width=True)

fig_scenario = px.bar(
    scenario_data,
    x="시나리오",
    y="손익",
    text="손익",
    title="시나리오별 예상 손익"
)

st.plotly_chart(fig_scenario, use_container_width=True)

st.divider()

st.subheader("📊 비용과 손익분기 매출 비교")

bar_data = pd.DataFrame({
    "항목": ["총비용", "손익분기 필요 총매출"],
    "금액": [total_cost, break_even_gross_revenue]
})

fig_bar = px.bar(
    bar_data,
    x="항목",
    y="금액",
    text="금액",
    title="총비용 vs 손익분기 필요 총매출"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("📈 관객 수에 따른 손익 변화")

audience_range = list(range(0, int(max(break_even_admissions * 2, optimistic, 10000)) + 1000, 1000))

profit_data = pd.DataFrame({
    "관객 수": audience_range
})

profit_data["손익"] = profit_data["관객 수"] * producer_revenue_per_ticket - total_cost

fig_line = px.line(
    profit_data,
    x="관객 수",
    y="손익",
    title="관객 수 증가에 따른 예상 손익"
)

st.plotly_chart(fig_line, use_container_width=True)

st.divider()

st.subheader("🎞️ 가상 한국 독립영화 샘플 데이터")

sample_data = pd.DataFrame({
    "영화 제목": ["겨울 골목", "작은 방의 빛", "늦여름의 편지"],
    "제작비": [50000000, 90000000, 120000000],
    "마케팅비": [8000000, 15000000, 20000000],
    "예상 관객 수": [7000, 18000, 35000],
    "장르": ["드라마", "가족", "멜로"]
})

sample_data["총비용"] = sample_data["제작비"] + sample_data["마케팅비"]
sample_data["예상 총매출"] = sample_data["예상 관객 수"] * average_ticket_price

st.dataframe(sample_data, use_container_width=True)

fig_sample = px.bar(
    sample_data,
    x="영화 제목",
    y="예상 총매출",
    color="장르",
    title="가상 독립영화별 예상 총매출"
)

st.plotly_chart(fig_sample, use_container_width=True)

st.caption("※ 본 계산기는 교육용 예측 도구이며, 실제 영화 수익 구조와는 차이가 있을 수 있습니다.")
