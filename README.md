# CEO Confidence Index

A Python/NLP financial analytics project that analyzes annual reports and earnings-call transcripts of leading Indian listed companies to estimate management confidence over time.

## Core capabilities

- Financial document ingestion
- PDF text extraction
- Financial sentiment analysis with FinBERT
- Keyword tracking for AI, inflation, expansion, CapEx and risk
- Topic modeling with BERTopic
- CEO Confidence Index scoring
- Streamlit dashboard
- SQLite storage
- Automated tests with GitHub Actions

## Project status

This repository contains the initial production-oriented scaffold. The data directory intentionally contains no copyrighted annual reports; use publicly available reports from the relevant company investor-relations pages.

## Local setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py
streamlit run dashboard/app.py
```

## Data workflow

1. Add annual-report PDFs to `data/annual_reports/`.
2. Run `python process_reports.py` to extract and clean report text.
3. Run `python run_analysis.py` to calculate NLP metrics.
4. Start the dashboard with `streamlit run dashboard/app.py`.

## Confidence methodology

The score is a research proxy rather than an investment recommendation. It combines document sentiment with normalized signals from expansion, CapEx and AI language, while penalizing inflation and risk language. For serious research, validate the scoring weights against historical management guidance and market outcomes.

## License

MIT
