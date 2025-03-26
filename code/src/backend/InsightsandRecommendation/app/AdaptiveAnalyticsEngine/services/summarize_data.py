def summarize_data(new_data):
    transactions_summary = summarize_transactions(new_data["transactions"])
    app_activity_summary = _summarize_app_activity(new_data["app_activity"])
    return {
            "transactions_summary": transactions_summary,
            "app_activity_summary": app_activity_summary
            }


def summarize_transactions(transactions_df):
    """Summarizes transaction data for LLM consumption"""
    if transactions_df.empty:
        return {}

    return {
        'total_spent': transactions_df['Transaction_Amount'].sum(),
        'num_transactions': len(transactions_df),
        'merchant_categories': transactions_df.groupby('Merchant_Category')['Transaction_Amount'].agg(['sum', 'count']).to_dict(),
        'merchants': transactions_df.groupby('Merchant')['Transaction_Amount'].agg(['sum', 'count']).to_dict(),
        'largest_transaction': {
            'amount': transactions_df['Transaction_Amount'].max(),
            'merchant': transactions_df.loc[transactions_df['Transaction_Amount'].idxmax(), 'Merchant'],
            'merchant_category': transactions_df.loc[transactions_df['Transaction_Amount'].idxmax(), 'Merchant_Category']
        }
    }


def _summarize_app_activity(app_activity_df):
    """Summarizes app activity for LLM consumption"""
    if app_activity_df.empty:
        return {}

        # Summarize pages visited by combining all "visited" arrays across sessions
    pages_visited = (
        app_activity_df['visited']
        .explode()  # Flatten the lists in the 'visited' column
        .value_counts()
        .to_dict()
    )

    # Summarize total time spent across all sessions
    total_time_spent = app_activity_df['session_duration'].sum()

    # Return the summarized data
    return {
        'pages_visited': pages_visited,
        'total_time_spent': total_time_spent,
    }
