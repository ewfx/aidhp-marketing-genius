import json
from typing import Dict, List, Any
import pandas as pd

from app.InsightGenerator.AnalyzeSpendingPattern.AnalyzeSpendCategories import analyze_categories
from app.InsightGenerator.AnalyzeSpendingPattern.AnalyzeSpendingDiscipline import analyze_spending_discipline
from app.InsightGenerator.AnalyzeSpendingPattern.AnalyzeTimePatterns import analyze_time_patterns
from app.utils.GenerateContentService import generate_content


def analyze_spending_patterns(transactions: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Comprehensive analysis of customer spending patterns with advanced insights.
    Args:
        transactions (List[Dict[str, str]]): List of transaction dictionaries
    Returns:
        Dict containing detailed spending insights
    """

    # Convert transactions to DataFrame
    def prepare_transactions(transactions) -> pd.DataFrame:
        """
        Convert list of transaction dictionaries to cleaned DataFrame
        """
        if not transactions:
            return pd.DataFrame()

        # Create DataFrame
        df = pd.DataFrame(transactions)

        # Ensure required columns exist
        required_cols = ['Transaction_Amount', 'Transaction_Date', 'Merchant_Category']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Convert amount to numeric
        df['Transaction_Amount'] = pd.to_numeric(df['Transaction_Amount'], errors='coerce')

        # Parse date with flexible format
        df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')

        # Drop rows with invalid data
        df.dropna(subset=['Transaction_Amount', 'Transaction_Date'], inplace=True)
        return df

    # Perform Analyses
    try:
        transactions_df = prepare_transactions(transactions)

        # Category Analysis
        spending_category_analysis = analyze_categories(transactions_df)

        # Time-based Analysis
        time_analysis = analyze_time_patterns(transactions_df)

        # Spending Discipline
        discipline_analysis = analyze_spending_discipline(transactions_df)

        # Combine all insights
        combined_insights = {
            'spending_category_insights': spending_category_analysis,
            'time_based_patterns': time_analysis,
            'spending_discipline': discipline_analysis,
            'additional_insights': {
                'total_transactions': len(transactions_df),
                'date_range': {
                    'start': transactions_df['Transaction_Date'].min().strftime('%Y-%m-%d'),
                    'end': transactions_df['Transaction_Date'].max().strftime('%Y-%m-%d')
                }
            }
        }

        llm_insights = llm_analyze_spending_insights(combined_insights, transactions)
        comprehensive_report = {
            'statistical_spend_insights': combined_insights,
            'llm_analysis': llm_insights
        }
        return comprehensive_report

    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "status": "error"
        }


def llm_analyze_spending_insights(insights, transactions) -> Dict:
    """Detect potential major life events."""

    prompt = get_spending_analysis_prompt(insights=insights, transactions=transactions)

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


def get_spending_analysis_prompt(insights: Dict[str, Any], transactions: List[Dict[str, str]]) -> str:
    """
    Generate a comprehensive prompt for Gemini to analyze spending patterns and details.

    Args:
        insights (Dict[str, Any]): Pre-generated insights from Python analysis
        transactions (List[Dict[str, str]]): Raw transaction data

    Returns:
        str: Comprehensive prompt for Gemini API
    """

    # Prepare a detailed, structured prompt for comprehensive spending analysis
    prompt = f"""
As an advanced financial behavior analyst and data scientist, conduct an in-depth analysis of the following customer spending profile. 
Provide a comprehensive, nuanced interpretation of the spending patterns, leveraging both the pre-computed insights and the raw transaction data.

PRE-COMPUTED INSIGHTS SUMMARY:
{json.dumps(insights, indent=2)}

COMPREHENSIVE ANALYSIS REQUIREMENTS:
Your response must be a structured JSON object with the following top-level keys:
1. spending_profile
2. financial_behavior
3. risk_assessment
4. personalized_recommendations
5. anomaly_detection

Specific Analysis Dimensions:
A. Spending Profile:
   - Detailed breakdown of spending categories
   - Percentage allocation across different expense types
   - Identification of primary and secondary spending domains
   - Trend analysis of spending patterns

B. Financial Behavior:
   - Spending consistency and volatility
   - Income-to-spending ratio insights
   - Discretionary vs. essential spending patterns
   - Potential financial stress indicators

C. Risk Assessment:
   - Financial stability indicators
   - Potential overspending risk
   - Savings potential
   - Unexpected expense vulnerability

D. Personalized Recommendations:
   - Targeted budgeting suggestions
   - Potential areas for financial optimization
   - Savings and investment recommendations
   - Expense reduction strategies

E. Anomaly Detection:
   - Unusual spending patterns
   - Potential fraudulent activity indicators
   - Significant deviations from normal spending behavior

ADDITIONAL CONTEXT:
- Total Transactions: {insights.get('additional_insights', {}).get('total_transactions', 'N/A')}
- Date Range: {json.dumps(insights.get('additional_insights', {}).get('date_range', {}), indent=2)}

TRANSACTION DATA SAMPLE (First 10 transactions):
{json.dumps(transactions[:1000], indent=2)}

CRITICAL CONSTRAINTS FOR RESPONSE:
1. Use ONLY the provided data for analysis
2. Ensure 100% JSON response
3. Use clear, actionable language
4. Provide precise, quantifiable insights
5. Format MUST match the specified JSON structure

Respond ONLY with the structured JSON analysis. Do not include any explanatory text, comments, or markdown.
"""
    return prompt
