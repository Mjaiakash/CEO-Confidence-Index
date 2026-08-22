from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from config import OUTPUT_DIR

st.set_page_config(page_title="CEO Confidence Index", page_icon="📈", layout="wide")
st.title("CEO Confidence Index")
st.caption("NLP-based analysis of management language in Indian company disclosures.")

csv_path = OUTPUT_DIR / "confidence_index.csv"
if not csv_path.exists():
    st.info("No analysis results yet. Add PDFs to data/raw/annual_reports, then run process_reports.py and run_analysis.py.")
    st.stop()

df = pd.read_csv(csv_path)
if df.empty:
    st.stop()

companies = ["All"] + sorted(df["company"].dropna().unique().tolist())
selected = st.sidebar.selectbox("Company", companies)
filtered = df if selected == "All" else df[df["company"] == selected]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Documents", len(filtered))
c2.metric("Companies", filtered["company"].nunique())
c3.metric("Avg. confidence", f"{filtered['confidence'].mean():.1f}")
c4.metric("Avg. polarity", f"{filtered['polarity'].mean():.3f}")

trend = filtered.sort_values("year")
if not trend.empty:
    st.plotly_chart(px.line(trend, x="year", y="confidence", color="company", markers=True, title="CEO confidence over time"), use_container_width=True)

left, right = st.columns(2)
with left:
    mention_cols = ["AI", "Inflation", "Expansion", "CapEx", "Risk"]
    mentions = filtered[mention_cols].sum().sort_values(ascending=False).reset_index()
    mentions.columns = ["theme", "mentions"]
    st.plotly_chart(px.bar(mentions, x="theme", y="mentions", title="Strategic theme mentions"), use_container_width=True)
with right:
    sentiment = filtered[["positive", "negative", "neutral"]].mean().sort_values(ascending=False).reset_index()
    sentiment.columns = ["sentiment", "score"]
    st.plotly_chart(px.bar(sentiment, x="sentiment", y="score", title="Average sentiment mix"), use_container_width=True)

st.subheader("Underlying analysis")
st.dataframe(filtered.sort_values(["year", "company"]), use_container_width=True)
