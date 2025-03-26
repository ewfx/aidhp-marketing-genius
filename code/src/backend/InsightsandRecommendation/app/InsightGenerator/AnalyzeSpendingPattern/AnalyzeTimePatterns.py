import pandas as pd
from datetime import datetime, timedelta


def analyze_time_patterns(df: pd.DataFrame):
    """
    Analyze spending patterns for the last 12 months and last 12 weeks

    Args:
        df (pd.DataFrame): DataFrame with Transaction_Date and Transaction_Amount columns

    Returns:
        Dict containing monthly and weekly spending statistics
    """
    # Ensure Transaction_Date is datetime
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])

    # Find the most recent date in the dataset
    most_recent_date = df['Transaction_Date'].max()

    # JSON serializable conversion function
    def convert_to_serializable(obj):
        """Convert Timestamp, Period, and numeric objects to JSON-friendly format"""
        if isinstance(obj, (pd.Timestamp, pd.Period)):
            return str(obj)
        if isinstance(obj, (int, float)):
            return obj
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='records')
        if isinstance(obj, pd.Series):
            return obj.to_dict()
        return str(obj)

    # Monthly Spending Analysis for Last 12 Months
    def get_monthly_spending():
        # Filter for last 12 months
        twelve_months_ago = most_recent_date - pd.DateOffset(months=12)
        monthly_df = df[df['Transaction_Date'] >= twelve_months_ago]

        # Group by month
        monthly_spending = monthly_df.groupby(monthly_df['Transaction_Date'].dt.to_period('M'))[
            'Transaction_Amount'].agg([
            ('total_monthly_spend', 'sum'),
            ('avg_daily_spend', 'mean'),
            ('transaction_count', 'count'),
            ('min_spend', 'min'),
            ('max_spend', 'max')
        ]).sort_index()

        # Add percentage change
        monthly_spending['month_over_month_change'] = monthly_spending['total_monthly_spend'].pct_change() * 100
        monthly_spending = monthly_spending.round(0)
        return monthly_spending

    # Weekly Spending Analysis for Last 12 Weeks
    def get_weekly_spending():
        # Filter for last 12 weeks
        twelve_weeks_ago = most_recent_date - timedelta(weeks=12)
        weekly_df = df[df['Transaction_Date'] >= twelve_weeks_ago]

        # Group by week
        weekly_spending = weekly_df.groupby(weekly_df['Transaction_Date'].dt.to_period('W'))['Transaction_Amount'].agg([
            ('total_weekly_spend', 'sum'),
            ('avg_daily_spend', 'mean'),
            ('transaction_count', 'count'),
            ('min_spend', 'min'),
            ('max_spend', 'max')
        ]).sort_index()

        # Add percentage change
        weekly_spending['week_over_week_change'] = weekly_spending['total_weekly_spend'].pct_change() * 100
        weekly_spending = weekly_spending.round(0)
        return weekly_spending

    # Compile results
    results = {
        'metadata': {
            'most_recent_date': convert_to_serializable(most_recent_date),
            'analysis_period_start': {
                '12_months_ago': convert_to_serializable(most_recent_date - pd.DateOffset(months=12)),
                '12_weeks_ago': convert_to_serializable(most_recent_date - timedelta(weeks=12))
            }
        }
    }

    # Add monthly spending if data is available
    try:
        monthly_data = get_monthly_spending()
        if not monthly_data.empty:
            results['monthly_spending'] = convert_to_serializable(monthly_data)
        else:
            results['monthly_spending'] = None
    except Exception as e:
        results['monthly_spending'] = {
            'error': str(e),
            'available_months': len(df['Transaction_Date'].dt.to_period('M').unique())
        }

    # Add weekly spending if data is available
    try:
        weekly_data = get_weekly_spending()
        if not weekly_data.empty:
            results['weekly_spending'] = convert_to_serializable(weekly_data)
        else:
            results['weekly_spending'] = None
    except Exception as e:
        results['weekly_spending'] = {
            'error': str(e),
            'available_weeks': len(df['Transaction_Date'].dt.to_period('W').unique())
        }

    return results
