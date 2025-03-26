import pandas as pd
from app.InsightGenerator.AnalyzeSpendingPattern.MerchantServiceEssence import categorize_merchant


def analyze_spending_discipline(transactions_df: pd.DataFrame):
    """
    Perform a comprehensive analysis of spending discipline using detailed merchant categorization.
    Parameters:
    df (pd.DataFrame): DataFrame containing transaction data
    Returns:
    dict: Comprehensive spending analysis metrics
    """

    # Categorize if merchant in transaction is essential or not
    def categorize_transaction(merchant):
        return categorize_merchant(merchant)

    # Add spending type columns
    transactions_df['Spending_Type'] = transactions_df['Merchant'].apply(categorize_transaction)

    # Spending volatility (coefficient of variation)
    spending_volatility = round(
        (transactions_df['Transaction_Amount'].std() / transactions_df['Transaction_Amount'].mean()), 2)

    # Transaction frequency (average transactions per day)
    date_range = (transactions_df['Transaction_Date'].max() - transactions_df['Transaction_Date'].min()).days + 1
    transaction_frequency = round(len(transactions_df) / date_range, 2)

    # Detailed spending breakdown
    spending_breakdown = transactions_df.groupby(['Spending_Type', 'Merchant_Category'])['Transaction_Amount'].agg([
        ('total_spend', 'sum'),
        ('transaction_count', 'count'),
        ('avg_transaction', 'mean'),
        ('percentage', lambda x: (x.sum() / transactions_df['Transaction_Amount'].sum() * 100).round(2))
    ]).reset_index()

    # Spending trend analysis
    transactions_df['Transaction_Month'] = pd.to_datetime(transactions_df['Transaction_Date']).dt.to_period('M').astype(
        str)
    monthly_spending = transactions_df.groupby(['Transaction_Month', 'Spending_Type'])[
        'Transaction_Amount'].sum().unstack()
    monthly_spending = monthly_spending.round(2)
    # Spending discipline metrics
    discipline_metrics = {
        'spending_volatility': spending_volatility,
        'transaction_frequency': transaction_frequency,
        'spending_breakdown': spending_breakdown.to_dict(orient='records'),
        'monthly_spending_trend': monthly_spending.to_dict(),
        'average_monthly_spending': monthly_spending.mean().tolist(),
        'spending_type_distribution': (
            spending_breakdown.groupby('Spending_Type')['total_spend']
            .sum()
            .apply(lambda x: x / spending_breakdown['total_spend'].sum() * 100)
            .to_dict()
        )
    }
    return discipline_metrics
