# JobShield AI

JobShield AI is a Flask web application that helps users evaluate whether a job posting looks legitimate, suspicious, or fraudulent. It combines a machine learning classifier with rule-based scam detection so the result is both fast and explainable.

## Overview

The app takes a pasted job description, runs it through a trained TF-IDF + Random Forest model, then checks the same text for common fraud signals such as:

- requests for personal documents or bank details
- personal email addresses instead of company domains
- upfront fees or deposits
- unrealistic earning promises
- pressure tactics like "apply immediately"
- vague company claims with no verifiable website
- WhatsApp or Telegram-only contact methods

That hybrid approach allows the app to return one of three outcomes:

- `REAL JOB`
- `SUSPICIOUS JOB`
- `FAKE JOB`

## Why This Project Matters

Fake job listings often rely on urgency, vague branding, and requests for sensitive information. JobShield AI is built as a lightweight safety layer for students, freshers, and general job seekers who want a quick first-pass screening before responding to a listing.

## Features

- Flask-based web interface for quick copy-paste analysis
- Machine learning fraud classification using TF-IDF and Random Forest
- Rule-based red flag detection for better transparency
- Final risk scoring with confidence and severity labels
- Clear UI feedback showing detected warning signs

## How It Works

### 1. Model Training

The training script in [model.py](/media/arsalan/50EEBAD1EEBAAE9A1/Projects/jobshield-ai/model.py) loads `fake_job_postings.csv`, merges text-heavy columns, vectorizes the text, trains the classifier, and saves the generated artifacts.

Training flow:

1. Load the dataset
2. Combine `title`, `company_profile`, `description`, and `requirements`
3. Build a TF-IDF feature matrix with up to `5000` features
4. Split the data into train and test sets
5. Train a `RandomForestClassifier`
6. Print evaluation metrics
7. Save `model.pkl` and `tfidf.pkl`

### 2. Prediction Layer

The Flask app in [app.py](/media/arsalan/50EEBAD1EEBAAE9A1/Projects/jobshield-ai/app.py) loads the saved model artifacts and predicts whether a submitted job posting appears fraudulent.

### 3. Rule-Based Safety Checks

The same request is also scanned for suspicious language patterns and scam markers. If enough red flags are found, the rule-based logic can override the raw ML prediction to produce a stronger warning.

### 4. Final Decision Logic

- `2+` red flags: `FAKE JOB`
- `1` red flag: `SUSPICIOUS JOB`
- `0` red flags and model predicts fraud: `FAKE JOB`
- otherwise: `REAL JOB`

## Tech Stack

- Python
- Flask
- pandas
- NumPy
- scikit-learn
- HTML + inline CSS

## Project Structure

```text
jobshield-ai/
├── app.py
├── model.py
├── fake_job_postings.csv
├── model.pkl
├── tfidf.pkl
├── templates/
│   └── index.html
├── .gitignore
├── requirements.txt
└── README.md
```

## File Guide

- [app.py](/media/arsalan/50EEBAD1EEBAAE9A1/Projects/jobshield-ai/app.py): Flask app, routing, prediction flow, red flag detection, and final decision logic
- [model.py](/media/arsalan/50EEBAD1EEBAAE9A1/Projects/jobshield-ai/model.py): training script that creates the saved model artifacts
- [templates/index.html](/media/arsalan/50EEBAD1EEBAAE9A1/Projects/jobshield-ai/templates/index.html): single-page interface for entering job text and viewing results
- `fake_job_postings.csv`: training dataset used to build the model
- `model.pkl`: saved Random Forest classifier
- `tfidf.pkl`: saved TF-IDF vectorizer

## Dataset Snapshot

Based on the included CSV:

- rows: about `17,886`
- columns: `18`
- target column: `fraudulent`

The current model uses these text fields:

- `title`
- `company_profile`
- `description`
- `requirements`

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate model artifacts

If `model.pkl` and `tfidf.pkl` are not present, train them first:

```bash
python model.py
```

### 4. Run the app

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Usage

1. Start the Flask server
2. Open the local web app in your browser
3. Paste a full job description into the text area
4. Click `Analyze Job Posting`
5. Review the prediction, confidence, risk level, and detected red flags

## Current Strengths

- Easy to run locally
- Combines ML with explainable rule-based checks
- Clear beginner-friendly interface
- Good portfolio project for applied NLP and scam detection

## Current Limitations

- Styling is embedded directly in the template
- No automated tests are included yet
- Dependency installation is simple, but the project still has no environment pinning beyond the basic `requirements.txt`
- Model loading assumes local pickle files are already available
- Rule-based heuristics may need tuning for different regions and scam patterns

## GitHub Readiness Notes

Before pushing this project, these repo hygiene points matter:

- do not commit `venv/`
- do not commit `__pycache__/`
- do not commit regenerated `.pkl` artifacts unless you intentionally want prebuilt model files in the repo
- keep the dataset only if you are comfortable with the repository size

The `.gitignore` in this project has been corrected to ignore common generated Python files and local environment folders.

## Suggested Next Improvements

- move CSS into a `static/` directory
- add tests for `check_red_flags()`
- improve model evaluation and error handling
- add deployment instructions for Render or Railway
- support URL-based or file-based job post analysis

## License

Add a license before publishing publicly so GitHub users know how the project can be used.
