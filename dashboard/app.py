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
from preprocessing.clean_text import clean_text
from preprocessing.pdf_parser import extract_text
from preprocessing.process_reports import parse_metadata

DEFAULT_REPORT = ROOT_DIR / "data" / "default" / "annual-report-2025-2026.pdf"
DEFAULT_DISPLAY_NAME = "TCS Integrated Annual Report 2025–26"

st.set_page_config(page_title="CEO Confidence Index", page_icon="📈", layout="wide")

st.title("CEO Confidence Index")
st.caption("NLP-based analysis of management language in Indian company disclosures.")


def analyze_pdf_path(pdf_path: Path, display_name: str | None = None) -> dict:
    """Analyze one PDF and return dashboard metrics."""
    text = clean_text(extract_text(pdf_path))
    company, year = parse_metadata(pdf_path)
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
        "filename": display_name or pdf_path.name,
    }


def persist_result(row: dict) -> None:
    """Append/replace one record in writable app storage."""
    csv_path = OUTPUT_DIR / "confidence_index.csv"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    existing = pd.read_csv(csv_path) if csv_path.exists() else pd.DataFrame()
    incoming = pd.DataFrame([row])
    combined = pd.concat([existing, incoming], ignore_index=True)
    combined = combined.drop_duplicates(subset=["filename"], keep="last")
    combined.to_csv(csv_path, index=False)


def ensure_default_report() -> None:
    """Make the bundled TCS FY2025-26 report the default dashboard document."""
    if not DEFAULT_REPORT.exists():
        return

    csv_path = OUTPUT_DIR / "confidence_index.csv"
    try:
        current = pd.read_csv(csv_path) if csv_path.exists() else pd.DataFrame()
    except Exception:
        current = pd.DataFrame()

    if "filename" in current.columns and DEFAULT_DISPLAY_NAME in current["filename"].astype(str).tolist():
        return

    try:
        result = analyze_pdf_path(DEFAULT_REPORT, DEFAULT_DISPLAY_NAME)
        persist_result(result)
    except Exception as exc:
        st.warning(f"The default report could not be analyzed yet: {exc}")


ensure_default_report()

with st.sidebar:
    st.header("Report selection")
    st.success("Default document loaded")
    st.caption(DEFAULT_DISPLAY_NAME)

    st.divider()
    st.subheader("Use another report")
    uploads = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload another annual report whenever you want to change or expand the analysis set.",
    )

    if st.button("Analyze uploaded report(s)", type="primary", disabled=not uploads):
        progress = st.progress(0.0)
        errors: list[str] = []

        for index, uploaded in enumerate(uploads):
            try:
                safe_name = Path(uploaded.name).name
                pdf_path = REPORT_DIR / safe_name
                pdf_path.write_bytes(uploaded.getvalue())
                result = analyze_pdf_path(pdf_path, safe_name)
                persist_result(result)
            except Exception as exc:
                errors.append(f"{uploaded.name}: {exc}")
            progress.progress((index + 1) / len(uploads))

        if errors:
            for error in errors:
                st.error(error)
        else:
            st.success(f"Analyzed {len(uploads)} uploaded report(s).")
        st.rerun()

csv_path = OUTPUT_DIR / "confidence_index.csv"
if not csv_path.exists():
    st.info("The default report is being prepared. Refresh the page if this message remains.")
    st.stop()

df = pd.read_csv(csv_path)
if df.empty:
    st.info("No analysis records are available yet.")
    st.stop()

companies = ["All"] + sorted(df["company"].dropna().unique().tolist())
selected = st.sidebar.selectbox("Company", companies)
filtered = df if selected == "All" else df[df["company"] == selected]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Documents", len(filtered))
c2.metric("Companies", filtered["company"].nunique())
c3.metric("Avg. confidence", f"{filtered['confidence'].mean():.1f}")
c4.metric("Avg. polarity", f"{filtered['polarity'].mean():.3f}")

if not filtered.empty and filtered["year"].notna().any():
    trend = filtered.sort_values("year")
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
    sentiment = filtered[["positive", "negative", "neutral"]].mean().sort_values(ascending=False).reset_index()
    sentiment.columns = ["sentiment", "score"]
    st.plotly_chart(
        px.bar(sentiment, x="sentiment", y="score", title="Average sentiment mix"),
        use_container_width=True,
    )

st.subheader("Documents in the index")
st.dataframe(
    filtered.sort_values(["year", "company"], na_position="last"),
    use_container_width=True,
    hide_index=True,
)
