# CEO Confidence Index

An end-to-end NLP and financial text analytics project that analyzes annual reports and earnings-call transcripts of major Indian listed companies to estimate management confidence over time.

## What it measures

- Positive vs. negative financial sentiment
- AI and automation mentions
- Inflation and cost-pressure mentions
- Expansion and capacity language
- Capital expenditure (CapEx) language
- Risk and uncertainty language
- A transparent 0–100 CEO Confidence Score

## Architecture

```text
Annual reports / transcripts
          |
          v
PDF/text ingestion
          |
          v
Cleaning + section extraction
          |
          +------> Keyword engine
          |
          +------> FinBERT sentiment
          |
          v
Confidence scoring
          |
          v
CSV / Excel outputs
          |
          v
Streamlit dashboard
```

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

For local FinBERT use, install the spaCy model as well:

```bash
python -m spacy download en_core_web_sm
```

Add public-company annual report PDFs to `data/raw/annual_reports/` using filenames such as:

```text
Reliance_2024.pdf
TCS_2024.pdf
Infosys_2024.pdf
```

Then run:

```bash
python preprocessing/process_reports.py
python run_analysis.py
streamlit run dashboard/app.py
```

## Important research note

The confidence formula in `nlp/confidence.py` is a transparent baseline heuristic for portfolio/research use. It is not a validated investment signal and should not be treated as financial advice. For a research paper, calibrate the index against an independently defined outcome and run robustness tests.

## Data policy

Do not commit third-party annual reports or transcripts to this repository. Store local source files under the ignored `data/raw/` directories and retain source URLs/metadata separately.
