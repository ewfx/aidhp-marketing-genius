from typing import Dict
import json
from app.utils.GenerateContentService import generate_content


def analyze_life_stage(data: Dict) -> Dict:
    """Analyze and predict customer life stage"""

    prompt = f"""
        As a financial analyst specializing in customer segmentation, analyze this customer data to determine the most likely life stage(s) the customer is in.

        Customer Information:
        {json.dumps(data['customer_info'], indent=2)}

        Transaction Data (Complete Records):
        {json.dumps(data['transactions'], indent=2)}

        Based on this information:
        1. Identify the most probable life stage(s) this customer is in (e.g., young adult, family formation, empty nester, retirement)
        2. Provide confidence level for each life stage prediction
        3. List key indicators from the data that support your conclusion
        4. Explain any ambiguities or alternative interpretations
        5. Identify any notable spending patterns or financial behaviors

        Format your response as JSON with keys: 'primary_life_stage', 'alternative_life_stages', 'confidence_level', 'key_indicators', 'reasoning'
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