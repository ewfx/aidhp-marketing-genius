import json
from typing import Dict
from app.utils.GenerateContentService import generate_content


def detect_life_events(data: Dict) -> Dict:
    """Detect potential major life events."""

    prompt = f"""
        As a financial analyst specializing in customer journey mapping, analyze these transaction patterns to identify potential major life events.

        Customer Information:
        {json.dumps(data['customer_info'], indent=2)}

        Transaction Data (Complete Records):
        {json.dumps(data['transactions'], indent=2)}

        Please identify:
        1. Any likely major life events suggested by these transactions (e.g., moving, new job, marriage, children, travel)
        2. The approximate timing of these events
        3. The probability that these events occurred
        4. The specific transactions or patterns that support each conclusion

        Format your response as JSON with keys: 'detected_events', where each event is an object with 'event_type', 'timing', 'probability', 'supporting_evidence'
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