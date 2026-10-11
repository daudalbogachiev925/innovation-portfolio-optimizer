import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

API = os.getenv("API_URL", "http://api:8000")
st.set_page_config(page_title="Innovation Portfolio", layout="wide")
st.title("Innovation Portfolio Optimizer")

@st.cache_data(ttl=15)
def fetch(path):
    return requests.get(f"{API}{path}").json()

projects = pd.DataFrame(fetch("/api/projects"))
if projects.empty:
    st.warning("Нет проектов")
    st.stop()

st.subheader("BCG-матрица")
projects["growth"] = projects.expected_return_m / projects.investment_m
st.plotly_chart(px.scatter(projects, x="strategic_fit", y="growth",
                            size="investment_m", color="risk_class",
                            hover_data=["code","name"]))

budget = st.sidebar.slider("Бюджет, M", 10.0, 500.0, 100.0)
max_hr = st.sidebar.slider("Макс. доля high-risk", 0.0, 0.6, 0.3)

if st.sidebar.button("Оптимизировать"):
    r = requests.post(f"{API}/api/optimize", json={
        "budget": budget, "max_high_risk_share": max_hr}).json()
    st.session_state["opt"] = r

if "opt" in st.session_state:
    o = st.session_state["opt"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Проектов", len(o["projects"]))
    c2.metric("Инвестиции, M", f"{o['total_investment']:.1f}")
    c3.metric("ROV, M", f"{o['total_rov']:.1f}")

    df = pd.DataFrame(o["projects"])
    st.dataframe(df[["code","name","investment_m","risk_class","expected_value","roi"]])

    st.subheader("Распределение по риску")
    rb = pd.DataFrame([{"risk": k, "investment": v}
                       for k, v in o["risk_breakdown"].items()])
    st.plotly_chart(px.pie(rb, names="risk", values="investment"))
