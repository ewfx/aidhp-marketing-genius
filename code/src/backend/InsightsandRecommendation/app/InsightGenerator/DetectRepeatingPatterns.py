import pandas as pd
import json
from typing import Dict
from app.utils.GenerateContentService import generate_content

def detect_repeating_patterns(transactions: pd.DataFrame) -> Dict:
    """Identify repeating transaction patterns."""

    # Prepare merchant frequency analysis
    merchant_frequency = transactions.groupby('Merchant')['Transaction_Amount'].agg(['count', 'mean']).sort_values(
        'count', ascending=False)

    # Category frequency analysis
    category_frequency = transactions.groupby('Transaction_Detail')['Transaction_Amount'].agg(
        ['count', 'mean']).sort_values('count', ascending=False)

    # Look for day-of-week or day-of-month patterns
    transactions['Transaction_Date'] = pd.to_datetime(transactions['Transaction_Date'])
    transactions['day_of_week'] = transactions['Transaction_Date'].dt.day_name()
    transactions['day_of_month'] = transactions['Transaction_Date'].dt.day

    dow_pattern = transactions.groupby('day_of_week')['Transaction_Amount'].agg(['count', 'sum', 'mean'])
    dom_pattern = transactions.groupby('day_of_month')['Transaction_Amount'].agg(['count', 'sum', 'mean'])

    prompt = f"""
    As a data scientist specializing in behavioral pattern recognition, analyze these transaction data to identify repeating patterns in this customer's financial behavior.

    Most Frequent Merchants:
    {merchant_frequency.head(10).to_string() if not merchant_frequency.empty else "None found"}

    Most Frequent Categories:
    {category_frequency.head(10).to_string() if not category_frequency.empty else "None found"}

    Day of Week Patterns:
    {dow_pattern.to_string() if not dow_pattern.empty else "None found"}

    Day of Month Patterns:
    {dom_pattern.head(10).to_string() if not dom_pattern.empty else "None found"}

    Please identify:
    1. Regular recurring transactions (subscriptions, bills, etc.)
    2. Shopping routines or habits
    3. Timing patterns (weekly, biweekly, monthly, etc.)
    4. Category-specific repeat behaviors
    5. The strength/consistency of each identified pattern

    Format your response as JSON with keys: 'recurring_transactions', 'shopping_routines', 'timing_patterns', 'category_patterns', 'pattern_insights'
    """

    # Call Gemini API
    response = generate_content(prompt, json_response=True)

    # Parse response
    try:
        result = json.loads(response)
        return result
    except json.JSONDecodeError:
        # Handle case where response isn't valid JSON
        return {
            "error": "Could not parse Gemini response",
            "raw_response": response.text
        }
