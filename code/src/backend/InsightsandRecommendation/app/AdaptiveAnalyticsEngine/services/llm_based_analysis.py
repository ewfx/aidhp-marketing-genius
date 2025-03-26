import json
from app.utils.GenerateContentService import generate_content


def prepare_llm_context(historical_context, new_data_summary):
    """Prepares context for LLM analysis with specific customer data fields"""

    customer_data_fields = ["life_stage", "life_events", "spending_patterns", "retention_risk"]

    llm_prompt = f"""

You are an advanced AI analysis engine specializing in detecting meaningful changes in customer profiles by comparing historical data with recent data. Your primary goal is to identify significant shifts in customer behavior, characteristics, and metrics.

Input Context
You will receive 2 key pieces of information:
1. Historical Customer Profile: Comprehensive data about the customer's past behaviors, characteristics, and metrics
2. New Data Summary: Condensed insights from recent customer activities

Historical Customer Profile: {historical_context}
New Data Summary: {new_data_summary}

Analysis Mandate
- Systematically compare historical profile with recent data
- Detect meaningful changes across multiple dimensions
- Quantify the magnitude and significance of detected changes

Response Requirements
Produce a structured JSON response with EXACTLY the following mandatory format:

```json
{{
    "profile_change_summary": {{
        "total_changes_detected": integer,
        "change_significance": "minor/moderate/substantial",
        "changed_metrics": [
            {{
                "metric_name": "string (MUST be one of: life_stage, life_events, spending_patterns, retention_risk)",
                "old_value": "mixed",
                "new_value": "mixed", 
                "change_percentage": "number",
                "change_significance": "minor/significant",
                "confidence_level": "low/medium/high",
                "potential_implications": [
                    "string describing possible reasons or impacts"
                ]
            }}
        ]
    }},
    "overall_profile_shift": {{
        "primary_direction": "positive/negative/neutral",
        "key_observations": [
            "string highlighting main insights"
        ]
    }}
}}
```

Mandatory Analysis Fields
You MUST ONLY analyze and report changes on these specific customer data fields:
{customer_data_fields}

Key Analysis Guidelines
1. Each change must be mapped to one of the specified customer data fields
2. If no significant changes are detected, return an empty 'changed_metrics' list
3. Changes should be quantified and rationalized
4. Maintain objectivity and data-driven insights

Analytical Constraints
- Strictly use the specified customer data fields
- Provide clear rationale for detected changes
- Highlight actionable insights
- Maintain high analytical precision

Output Expectations
- Comprehensive yet concise analysis
- Perfectly structured JSON format
- Actionable and meaningful insights
- Balanced interpretation of data shifts

Proceed with a meticulous and intelligent analysis of the customer profile transformation."""

    return llm_prompt

def analyze_with_llm(prompt):
    """Sends data to LLM for analysis and insights generation"""

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
