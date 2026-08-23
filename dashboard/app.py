from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Streamlit Cloud executes dashboard/app.py directly, so add the repository root.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import plotly.express as px
import streamlit as st

from config import OUTPUT_DIR, REPORT_DIR, PROCESSED_DIR
from nlp.confidence import calculate_confidence
from nlp.keywords import keyword_frequency
from nlp.sentiment import analyze_sentiment
from preprocessing.cleaner import clean_text
from preprocessing.parser import extract_text
from process_reports import parse_metadata

st.set_page_config(page_title="CEO Confidence Index", page_icon="📈", layout="wide")

st.title("CEO Confidence Index")
st.caption("NLP-based analysis of management language in Indian company disclosures.")


def analyze_uploaded_pdf(uploaded_file: Any) -> dict:
    """Persist and analyze one uploaded PDF without requiring a Git commit."""
    safe_name = Path(uploaded_file.name).name
    pdf_path = REPORT_DIR / safe_name
    pdf_path.write_bytes(uploaded_file.getvalue())

    text = clean_text(extract_text(pdf_path))
    processed_path = PROCESSED_DIR / f"{pdf_path.stem}.txt"
    processed_path.write_text(text, encoding="utf-8")

    company, year = parse_metadata(pdf_path.name)
    sentiment = analyze_sentiment(text)
    keywords = keyword_frequency(text)
    confidence = calculate_confidence(sentiment, keywords)

    return {
        "company": company,
        "year": year,
        "confidence": confidence,
        "positive": sentiment["positive"],
        "negative": sentiment["negative"],
        "neutral": sentiment["neutral"],
        "polarity": round(sentiment["positive"] - sentiment["negative"], 4),
        "AI": keywords["AI"],
        "Inflation": keywords["Inflation"],
        "Expansion": keywords["Expansion"],
        "CapEx": keywords["CapEx"],
        "Risk": keywords["Risk"],
        "filename": safe_name,
    }


def persist_result(row: dict) -> None:
    """Append/replace a dashboard record in the deployed app's writable storage."""
    csv_path = OUTPUT_DIR / "confidence_index.csv"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    existing = pd.read_csv(csv_path) if csv_path.exists() else pd.DataFrame()
    incoming = pd.DataFrame([row])
    combined = pd.concat([existing, incoming], ignore_index=True)

    if "filename" in combined.columns:
        combined = combined.drop_duplicates(subset=["filename"], keep="last")

    combined.to_csv(csv_path, index=False)


with st.sidebar:
    st.header("Upload reports")
    st.write("Upload annual-report PDFs directly from your phone or computer.")
    uploads = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Use filenames such as TCS_2024.pdf so the app can infer company and year.",
    )

    if st.button("Analyze uploaded reports", type="primary", disabled=not uploads):
        progress = st.progress(0.0)
        errors: list[str] = []

        for index, uploaded in enumerate(uploads):
            try:
                result = analyze_uploaded_pdf(uploaded)
                persist_result(result)
            except Exception as exc:
                errors.append(f"{uploaded.name}: {exc}")
            progress.progress((index + 1) / len(uploads))

        if errors:
            for error in errors:
                st.error(error)
        else:
            st.success(f"Analyzed {len(uploads)} report(s).")
        st.rerun()

csv_path = OUTPUT_DIR / "confidence_index.csv"

if not csv_path.exists():
    st.info(
        "No analysis results yet. Upload one or more annual-report PDFs in the sidebar "
        "and click **Analyze uploaded reports**."
    )
    st.stop()

df = pd.read_csv(csv_path)
if df.empty:
    st.info("The analysis file is empty. Upload a report to begin.")
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
    st.plotly_chart(
        px.line(
            trend,
            x="year",
            y="confidence",
            color="company",
            markers=True,
            title="CEO confidence over time",
        ),
        use_container_width=True,
    )

left, right = st.columns(2)
with left:
    mention_cols = ["AI", "Inflation", "Expansion", "CapEx", "Risk"]
    mentions = filtered[mention_cols].sum().sort_values(ascending=False).reset_index()
    mentions.columns = ["theme", "mentions"]
    st.plotly_chart(
        px.bar(mentions, x="theme", y="mentions", title="Strategic theme mentions"),
        use_container_width=True,
    )
with right:
    sentiment = (
        filtered[["positive", "negative", "neutral"]]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    sentiment.columns = ["sentiment", "score"]
    st.plotly_chart(
        px.bar(sentiment, x="sentiment", y="score", title="Average sentiment mix"),
        use_container_width=True,
    )

st.subheader("Underlying analysis")
st.dataframe(filtered.sort_values(["year", "company"], na_position="last"), use_container_width=True)
