# CSV/Excel Cleaning Tool (Python)

A Python-based script that automatically cleans and transforms messy Excel or CSV files — ideal for data analysts, freelancers, and business automation.

---

## Features

- ✅ **Removes duplicates**
- ✅ **Validates and standardizes email addresses**
- ✅ **Normalizes names and region formatting**
- ✅ **Parses and fixes date formats**
- ✅ **Cleans and converts revenue fields to numeric**
- ✅ **Aggregates revenue and notes for repeat entries**
- ✅ **Exports cleaned file as `.xlsx`**

---

## Folder Structure
CSV-Excel-Cleaning-Tool/
├── cleaner.py # Main script
├── input/ # Place raw messy files here
│ └── messy_file.xlsx
├── output/ # Cleaned Excel files will be saved here
├── .gitignore
└── README.md


---

## Requirements

Install dependencies:
```bash
pip install pandas openpyxl
