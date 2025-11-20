import pandas as pd
import os
from datetime import datetime

# =============================================================================
# CONFIGURATION: File paths setup
# =============================================================================

# Get the base directory (project root folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define path to raw Excel file
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw_data.xlsx')

# Define directory for processed output files
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed_data')

# Create processed_data folder if it doesn't exist
os.makedirs(PROCESSED_DIR, exist_ok=True)

# =============================================================================
# HEADER: Display script information
# =============================================================================

print("=" * 60)
print("Financial Dashboard - Data Processing")
print("=" * 60)
print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# =============================================================================
# STEP 1: LOAD DATA FROM EXCEL
# =============================================================================
print("Loading raw data from Excel...")

try:
    # Read each sheet from the Excel workbook
    transactions_df = pd.read_excel(RAW_DATA_PATH, sheet_name='Transactions')
    budget_df = pd.read_excel(RAW_DATA_PATH, sheet_name='Budget')
    invoices_df = pd.read_excel(RAW_DATA_PATH, sheet_name='Invoices')

    # Display confirmation with record counts
    print(f"Loaded Transactions: {len(transactions_df)} records")
    print(f"Loaded Budget: {len(budget_df)} records")
    print(f"Loaded Invoices: {len(invoices_df)} records")
    print()

except FileNotFoundError:
    # Handle case when Excel file doesn't exist
    print("Error: raw_data.xlsx not found!")
    print(f"Expected location: {RAW_DATA_PATH}")
    exit(1)

except Exception as e:
    # Handle any other errors during file reading
    print(f"❌ Error loading data: {e}")
    exit(1)

# =============================================================================
# STEP 2: PROCESS TRANSACTIONS
# Calculate profit and profit margin for each transaction
# =============================================================================

print("Processing Transactions...")

# Calculate Profit: Revenue minus Cost
transactions_df['Profit'] = transactions_df['Revenue'] - transactions_df['Cost']

# Calculate Margin as percentage: (Profit / Revenue) * 100
transactions_df['Margin_%'] = (
        transactions_df['Profit'] / transactions_df['Revenue'] * 100
).round(2)

# Extract Month in format "2024-01" for grouping
transactions_df['Month'] = pd.to_datetime(transactions_df['Date']).dt.to_period('M')

# Extract Year (e.g., 2024)
transactions_df['Year'] = pd.to_datetime(transactions_df['Date']).dt.year

# Sort all transactions by date (earliest first)
transactions_df = transactions_df.sort_values('Date')

# Display summary statistics
print(f"Calculated Profit and Margin for {len(transactions_df)} transactions")
print(f"Average Margin: {transactions_df['Margin_%'].mean():.2f}%")
print()

# =============================================================================
# STEP 3: BUDGET ANALYSIS
# Compare actual performance vs budget targets
# =============================================================================

print("Processing Budget Analysis...")

# Aggregate actual results by Department and Month
actual_summary = transactions_df.groupby(['Department', 'Month']).agg({
    'Revenue': 'sum',      # Total revenue per department per month
    'Cost': 'sum',         # Total cost per department per month
    'Profit': 'sum'        # Total profit per department per month
}).reset_index()

# Rename columns to distinguish from budget values
actual_summary.columns = [
    'Department', 'Month',
    'Actual_Revenue', 'Actual_Cost', 'Actual_Profit'
]

# Convert Budget Month column to Period format for matching
budget_df['Month'] = pd.to_datetime(budget_df['Month']).dt.to_period('M')

# Merge budget targets with actual results
# 'left' join keeps all budget records even if no actual data exists
budget_analysis = budget_df.merge(
    actual_summary,
    on=['Department', 'Month'],
    how='left'
)

# Replace missing values with 0 (months with no transactions)
budget_analysis[['Actual_Revenue', 'Actual_Cost', 'Actual_Profit']] = \
    budget_analysis[['Actual_Revenue', 'Actual_Cost', 'Actual_Profit']].fillna(0)

# Calculate variance: Actual - Budget (positive = over budget)
budget_analysis['Revenue_Variance'] = (
        budget_analysis['Actual_Revenue'] - budget_analysis['Budget_Revenue']
)

budget_analysis['Cost_Variance'] = (
        budget_analysis['Actual_Cost'] - budget_analysis['Budget_Cost']
)

# Calculate achievement percentage: (Actual / Budget) * 100
budget_analysis['Revenue_Achievement_%'] = (
        budget_analysis['Actual_Revenue'] / budget_analysis['Budget_Revenue'] * 100
).round(2)

# Display summary
print(f"Budget analysis completed for {len(budget_analysis)} department-months")
print(f"Average Revenue Achievement: {budget_analysis['Revenue_Achievement_%'].mean():.2f}%")
print()

# =============================================================================
# STEP 4: INVOICE PROCESSING
# Analyze invoice payment status and timing
# =============================================================================

print("Processing Invoices...")

# Convert date columns to proper datetime format
invoices_df['Date'] = pd.to_datetime(invoices_df['Date'])
invoices_df['Payment_Date'] = pd.to_datetime(
    invoices_df['Payment_Date'],
    errors='coerce'  # Convert invalid dates to NaT (Not a Time)
)

# Calculate number of days between invoice and payment
invoices_df['Days_to_Payment'] = (
        invoices_df['Payment_Date'] - invoices_df['Date']
).dt.days

# Split invoices by status for separate analysis
paid_invoices = invoices_df[invoices_df['Status'] == 'Paid']
pending_invoices = invoices_df[invoices_df['Status'] == 'Pending']

# Display invoice statistics
print(f"Invoices processed:")
print(f"Paid: {len(paid_invoices)} (Total: €{paid_invoices['Amount'].sum():,.0f})")
print(f"Pending: {len(pending_invoices)} (Total: €{pending_invoices['Amount'].sum():,.0f})")
print(f"Average payment time: {paid_invoices['Days_to_Payment'].mean():.1f} days")
print()

# =============================================================================
# STEP 5: SAVE PROCESSED DATA TO CSV FILES
# =============================================================================

print("Saving processed data...")

# Save processed transactions
transactions_output = os.path.join(PROCESSED_DIR, 'transactions_processed.csv')
transactions_df.to_csv(transactions_output, index=False)
print(f"Saved: transactions_processed.csv ({len(transactions_df)} rows)")

# Save budget analysis
budget_output = os.path.join(PROCESSED_DIR, 'budget_analysis.csv')
budget_analysis.to_csv(budget_output, index=False)
print(f"Saved: budget_analysis.csv ({len(budget_analysis)} rows)")

# Save invoice summary
invoices_output = os.path.join(PROCESSED_DIR, 'invoices_summary.csv')
invoices_df.to_csv(invoices_output, index=False)
print(f"Saved: invoices_summary.csv ({len(invoices_df)} rows)")

# =============================================================================
# COMPLETION MESSAGE
# =============================================================================

print()
print("=" * 60)
print("DATA PROCESSING COMPLETED SUCCESSFULLY!")
print("=" * 60)
print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()
print("Next step: Create dashboard with Streamlit")
print("Command: streamlit run dashboard/financial_dashboard.py")
