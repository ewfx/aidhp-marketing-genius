import pandas as pd

# Comprehensive Category Spending Analysis
def analyze_categories(df: pd.DataFrame):
    # Analysis dictionary to store different insights
    analysis = {}

    # Total Spending by Merchant Category
    category_spending = df.groupby('Merchant_Category')['Transaction_Amount'].agg(['sum', 'count']).reset_index()
    category_spending.columns = ['Merchant_Category', 'Total_Spending', 'Transaction_Count']
    category_spending['Average_Transaction'] = category_spending['Total_Spending'] / category_spending[
        'Transaction_Count']
    analysis['merchant_category_breakdown'] = category_spending.to_dict(orient='records')

    # Total Spending by Individual Merchant
    merchant_spending = df.groupby('Merchant')['Transaction_Amount'].agg(['sum', 'count']).reset_index()
    merchant_spending.columns = ['Merchant', 'Total_Spending', 'Transaction_Count']
    merchant_spending['Average_Transaction'] = merchant_spending['Total_Spending'] / merchant_spending[
        'Transaction_Count']

    # Excluding individual merchant analysis
    # analysis['merchant_breakdown'] = merchant_spending.to_dict(orient='records')

    # Top Merchant Categories by Total Spending
    top_categories = category_spending.sort_values('Total_Spending', ascending=False)
    analysis['top_merchant_categories'] = top_categories.head(3).to_dict(orient='records')

    # Basic Statistical Summary
    analysis['spending_summary'] = {
        'total_amount_spent': df['Transaction_Amount'].sum(),
        'average_transaction_amount': df['Transaction_Amount'].mean(),
        'median_transaction_amount': df['Transaction_Amount'].median(),
        'max_transaction_amount': df['Transaction_Amount'].max(),
        'min_transaction_amount': df['Transaction_Amount'].min()
    }

    return analysis
