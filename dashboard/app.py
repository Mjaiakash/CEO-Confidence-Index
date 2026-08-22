import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

from config import OUTPUT_DIR

st.set_page_config(page_title="CEO Confidence Index", page_icon="📈", layout="wide")
st.title("CEO Confidence Index")
st.caption("NLP analysis of management commentary. Scores are research indicators, not investment advice.")

results_path = OUTPUT_DIR / "analysis_results.json"
if not results_path.exists():
    st.info("No analysis data found. Add PDFs to data/annual_reports, then run process_reports.py and run_analysis.py.")
    st.stop()

data = json.loads(results_path.read_text(encoding="utf-8"))
df = pd.DataFrame(data)
if df.empty:
    st.warning("The analysis file is empty.")
    st.stop()

companies = sorted(df["company"].dropna().unique())
selected = st.sidebar.selectbox("Company", ["All"] + companies)
if selected != "All":
    view = df[df["company"] == selected].copy()
else:
    view = df.copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Reports", len(view))
c2.metric("Companies", view["company"].nunique())
c3.metric("Avg. Confidence", f"{view['confidence'].mean():.1f}")
c4.metric("Avg. Sentiment", f"{view['sentiment_score'].mean():.2f}")

if "year" in view.columns and view["year"].notna().any():
    trend = view.dropna(subset=["year"]).sort_values("year")
    fig = px.line(trend, x="year", y="confidence", color="company", markers=True,
                  title="CEO Confidence Trend")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    sentiment = view.groupby("company", as_index=False)["sentiment_score"].mean()
    fig = px.bar(sentiment, x="company", y="sentiment_score", title="Average Sentiment")
    st.plotly_chart(fig, use_container_width=True)
with right:
    keyword_cols = ["AI_mentions", "Inflation_mentions", "Expansion_mentions", "CapEx_mentions", "Risk_mentions"]
    totals = view[keyword_cols].sum().reset_index()
    totals.columns = ["category", "mentions"]
    fig = px.bar(totals, x="category", y="mentions", title="Key Theme Mentions")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Analysis Data")
st.dataframe(view.sort_values(["year", "company"], na_position="last"), use_container_width=True)
