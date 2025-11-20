# financial-dashboard
Automated Financial Controlling Dashboard for P&amp;L analysis with Python, Excel VBA, and PowerBI

## Overview
This project provides automated data processing and analysis for financial controlling, including:
- Transaction processing with profit and margin calculations
- Budget variance analysis
- Invoice payment tracking and analysis

## Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kelemano/financial-dashboard.git
cd financial-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Processing

Process raw financial data from Excel and generate CSV files:

```bash
python scripts/process_data.py
```

This script will:
- Load data from `data/raw_data.xlsx` (Transactions, Budget, Invoices sheets)
- Calculate profit and margin metrics
- Perform budget variance analysis
- Analyze invoice payment timing
- Export processed data to `data/processed_data/` as CSV files

### Output Files

The script generates three CSV files:
- `transactions_processed.csv` - Enriched transaction data with profit and margin calculations
- `budget_analysis.csv` - Budget variance and achievement analysis
- `invoices_summary.csv` - Invoice payment status and timing analysis

## Project Structure

```
financial-dashboard/
├── data/
│   ├── raw_data.xlsx           # Input: Raw financial data
│   └── processed_data/         # Output: Processed CSV files (generated)
├── scripts/
│   └── process_data.py         # Main data processing script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Next Steps

Create dashboard with Streamlit:
```bash
streamlit run dashboard/financial_dashboard.py
```
