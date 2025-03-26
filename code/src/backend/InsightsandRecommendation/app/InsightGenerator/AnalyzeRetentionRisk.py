from typing import Dict
import json
from app.utils.GenerateContentService import generate_content


def analyze_retention_risk(data: Dict) -> Dict:
    """Assess the risk of customer attrition."""

    prompt = f"""
    As a customer retention analyst, evaluate this customer's risk of attrition based on their data and transaction patterns.

    Customer Information:
    {json.dumps(data['customer_info'], indent=2)}

    Transaction Data (Complete Records):
    {json.dumps(data['transactions'], indent=2)}

    Based on this information:
    1. Assess this customer's overall attrition risk (low, medium, high)
    2. Identify key risk factors or protective factors
    3. Suggest the most effective retention strategies for this specific customer
    4. Estimate the probability of attrition in the next 6 months

    Format your response as JSON with keys: 'attrition_risk_level', 'risk_factors', 'protective_factors', 'retention_strategies', 'attrition_probability'
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
