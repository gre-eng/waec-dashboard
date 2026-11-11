# WAEC Nigeria — WASSCE Statistics Dashboard (2019–2021)

![HTML](https://img.shields.io/badge/Built%20With-HTML%20%2F%20CSS%20%2F%20JavaScript-informational)
![Python](https://img.shields.io/badge/Data%20Pipeline-Python%20%2F%20Pandas-blue)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)
![Data Source](https://img.shields.io/badge/Data%20Source-NBS%20Nigeria-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
[![DOI](https://zenodo.org/badge/1264381214.svg)](https://doi.org/10.5281/zenodo.24147242)

A sleek, fully interactive web dashboard that cleans, analyses and visualises West African Examinations Council (WAEC) school candidate statistics for Nigeria from 2019 to 2021. Built with Python for data processing and pure HTML/CSS/JavaScript for the front end — no frameworks, no dependencies beyond Chart.js.

**Live App →** [https://gre-eng.github.io/waec-dashboard/](https://gre-eng.github.io/waec-dashboard/)

**DOI →** [https://doi.org/10.5281/zenodo.24147242](https://doi.org/10.5281/zenodo.24147242)

---

## Table of Contents

- [Objective](#objective)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Key Findings](#key-findings)
- [Features](#features)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Data Source](#data-source)
- [Cite This Work](#cite-this-work)
- [Licence](#licence)
- [Author](#author)

---

## Objective

The goal of this project is to transform raw, multi-table WAEC public data into a clean, accessible, and visually compelling dashboard that:

- Reveals national and state-level trends in student performance over three years
- Highlights the gap between private and public school candidates
- Surfaces gender disparities in enrolment across school types
- Shows regional performance differences across Nigeria's six geo-zones
- Provides a practical student tool that predicts fail risk and delivers personalised improvement tips based on individual CA and exam scores

---

## Dataset

| Property | Detail |
|---|---|
| Source | National Bureau of Statistics (NBS), Nigeria |
| Dataset | WAEC WASSCE School Candidates Statistics |
| Years covered | 2019, 2020, 2021 |
| File format | Microsoft Excel (.xlsx) |
| Geographic coverage | 37 states including FCT Abuja |
| Key metrics | Total candidates sat, pass rates (5 credits including English and Mathematics), gender breakdown, private vs public school split, geo-zone performance |

The raw Excel file contains multiple side-by-side tables with merged cells, multi-row headers and unstandardised formatting — all of which are resolved in the data cleaning pipeline.

---

## Methodology

### 1. Data Extraction
The Excel file was loaded using `pandas` with `openpyxl` as the engine. The `Analysis` sheet was targeted as it contains the consolidated national and geo-zone summary tables.

### 2. Data Cleaning
- Merged cell headers were manually resolved by reassigning clean column names
- Corrupt header rows (rows 0 and 1) were dropped and the index was reset
- Indicator labels were standardised and reassigned to a clean `Indicator` column
- A custom `get_row()` function was written to extract specific metrics by indicator name and parent context, handling duplicate indicator names (e.g. multiple rows labelled `Private` or `Female` under different parent categories)

### 3. Metric Computation
Pass rates were computed as:

```
Pass Rate (%) = (Candidates who passed / Total candidates sat) × 100
```

This was calculated separately for private schools, public schools, and the overall national figure for each year.

Geo-zone pass rates were computed by combining private and public school pass figures for each zone before dividing by total candidates sat.

### 4. Visualisation
Cleaned metrics were serialised to JSON and injected directly into a self-contained HTML file using Python f-strings. Five Chart.js charts were built covering enrolment trends, pass rates, gender distribution, geo-zone performance and a state-level colour-coded heatmap table.

### 5. Student Predictor
A client-side JavaScript tool was built into the same HTML file. It accepts CA scores (0–30) and exam scores (0–70) per subject, computes a predicted grade using WAEC's grading scale, estimates a fail risk percentage based on the 45/100 pass threshold, and returns personalised improvement tips graded by performance level.

---

## Key Findings

**Enrolment**
- Total candidates sat declined slightly from 1.59 million in 2019 to 1.54 million in 2020, likely reflecting the disruption caused by COVID-19, before recovering to 1.56 million in 2021
- Public schools consistently produce more candidates than private schools across all three years

**Pass Rates**
- The national pass rate dropped marginally from 62.4% in 2019 to 62.0% in 2020 before rising sharply to 79.7% in 2021 — a 17.7 percentage point improvement in a single year
- Private school candidates consistently outperform public school candidates: 76.5% vs 50.9% in 2019, 74.8% vs 51.2% in 2020, and 86.6% vs 73.8% in 2021
- The gap between private and public pass rates narrowed significantly in 2021, suggesting improvements in public school performance

**Gender**
- In private schools, female candidates slightly outnumber male candidates across all three years
- In public schools, male candidates consistently outnumber female candidates, indicating a gender enrolment gap that persists in the public education system

**Geo-Zones**
- The South West zone consistently records the highest pass rates across all three years
- The North East zone consistently records the lowest pass rates, reflecting broader educational inequality between northern and southern Nigeria
- All six zones recorded significant improvements in 2021

**State Level**
- Sokoto (97.2%), Kebbi (96.7%) and Anambra (92.8%) recorded the highest private school pass rates in 2021
- Zamfara (36.1%) recorded the lowest private school pass rate in 2021
- Most states showed upward trends from 2019 to 2021, with notable recoveries in states that dipped in 2020

---

## Features

- **Interactive tab navigation** — switch between five chart views without page reload
- **Enrolment trend chart** — line chart showing private vs public candidates sat from 2019 to 2021
- **Pass rate chart** — grouped bar chart comparing private, public and overall pass rates by year
- **Gender distribution charts** — stacked bar charts for private and public schools side by side
- **Geo-zone chart** — grouped bar chart showing pass rates across Nigeria's six geo-political zones
- **State heatmap** — colour-coded table of all 37 states showing pass rates across all three years with trend indicators
- **Student performance predictor** — enter CA (max 30) and exam (max 70) scores per subject to get predicted grade, fail risk percentage and personalised improvement tips
- Input validation: negative numbers and out-of-range values are automatically blocked
- Improvement tips are graded across five levels (A through F) ensuring every student — including top performers — receives actionable guidance

---

## How to Run

### Option 1 — Open directly in your browser (no installation required)
Visit the live app: [https://gre-eng.github.io/waec-dashboard/](https://gre-eng.github.io/waec-dashboard/)

### Option 2 — Run locally from source

**Requirements**
- Python 3.8 or above
- pip

**Step 1 — Clone the repository**
```bash
git clone https://github.com/gre-eng/waec-dashboard.git
cd waec-dashboard
```

**Step 2 — Install dependencies**
```bash
pip install pandas openpyxl
```

**Step 3 — Add the dataset**

Place `WAEC_STATISTICS_2019-2021.xlsx` in the project root directory. The dataset is not included in this repository as it is sourced from the NBS public data portal.

**Step 4 — Run the Python script**
```bash
python waec_analysis.py
```

**Step 5 — Open the dashboard**

Open the generated `index.html` file in any modern browser (Chrome, Edge or Firefox recommended).

---

## Project Structure

```
waec-dashboard/
│
├── waec_analysis.py           # Python data cleaning and HTML generation script
├── index.html                 # Generated dashboard (served by GitHub Pages)
├── WAEC_STATISTICS_2019-2021.xlsx  # Source dataset (NBS — not included in repo)
├── LICENSE                    # MIT Licence
├── CITATION.cff               # Citation metadata
└── README.md                  # Project documentation
```

---

## Technologies Used

| Tool | Purpose |
|---|---|
| Python 3 | Data extraction and cleaning |
| pandas | DataFrame operations and Excel parsing |
| openpyxl | Excel file engine for pandas |
| Chart.js | Interactive browser charts |
| HTML / CSS / JavaScript | Dashboard front end |
| GitHub Pages | Free static site hosting |

---

## Data Source

This project uses publicly available data published by the **National Bureau of Statistics (NBS)** of Nigeria in partnership with the **West African Examinations Council (WAEC)**.

---

## Cite This Work

If you use this dashboard, please cite it using the DOI:

Umoh, G. P. (2026). *WAEC Nigeria — WASSCE Statistics Dashboard (2019–2021)* [Software]. Zenodo. https://doi.org/10.5281/zenodo.24147242

A `CITATION.cff` file is included in this repository.

---

## Licence

The code in this repository is released under the MIT Licence (see `LICENSE`). The underlying NBS/WAEC data is not covered by this licence and remains subject to its source's terms.

---

## Author

**Gregory Patrick Umoh**
[github.com/gre-eng](https://github.com/gre-eng)
