from typing import Dict
import json
import logging
from app.utils.GenerateContentService import generate_content

# Setup logging
logger = logging.getLogger(__name__)

def analyze_life_stage(data: Dict) -> Dict:
    """Analyze and predict customer life stage"""
    try:
        # Validate input data
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")
        if 'customer_info' not in data or 'transactions' not in data:
            raise ValueError("Input data must contain 'customer_info' and 'transactions' keys")

        prompt = f"""
            As a financial analyst specializing in customer segmentation, analyze this customer data to determine the most likely life stage(s) the customer is in.

            Customer Information:
            {json.dumps(data['customer_info'], indent=2)}

            Transaction Data (Complete Records):
            {json.dumps(data['transactions'], indent=2)}

            Analysis Instructions:
             - Identify primary and potential alternative life stages
             - Assign confidence levels (0-100%)
             - Highlight key indicators supporting life stage prediction
             - Explain reasoning and potential ambiguities

             Required Response Format:
             Use the following JSON Schema to structure your JSON response-
             {schema}

             Evaluation Criteria:
              - Depth of analysis
              - Quality of indicators
              - Clarity of reasoning
              - Statistical confidence of predictions
            """

        try:
            # Call Gemini API
            response = generate_content(prompt, json_response=True)
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return {
                "error": "Failed to generate content",
                "message": str(e)
            }

        # Parse response
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Gemini response: {str(e)}")
            logger.info(response)
            return {
                "error": "Could not parse Gemini response",
                "raw_response": response,
                "message": str(e)
            }

    except ValueError as e:
        logger.error(f"Input validation error: {str(e)}")
        return {
            "error": "Invalid input data",
            "message": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in analyze_life_stage: {str(e)}")
        return {
            "error": "Unexpected error",
            "message": str(e)
        }

schema = {
        "type": "object",
        "properties": {
            "primary_life_stage": {
                "type": "string",
                "enum": [
                    "student",
                    "young_adult",
                    "family_formation",
                    "mid_career",
                    "empty_nester",
                    "pre_retirement",
                    "retirement"
                ]
            },
            "alternative_life_stages": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "student",
                        "young_adult",
                        "family_formation",
                        "mid_career",
                        "empty_nester",
                        "pre_retirement",
                        "retirement"
                    ]
                }
            },
            "confidence_level": {
                "type": "object",
                "properties": {
                    "primary_stage": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "alternative_stages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "stage": {"type": "string"},
                                "confidence": {
                                    "type": "number",
                                    "minimum": 0,
                                    "maximum": 100
                                }
                            }
                        }
                    }
                }
            },
            "key_indicators": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "details": {"type": "string"},
                        "weight": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1
                        }
                    }
                }
            },
            "reasoning": {
                "type": "string",
                "maxLength": 1000
            }
        },
        "required": [
            "primary_life_stage",
            "alternative_life_stages",
            "confidence_level",
            "key_indicators",
            "reasoning"
        ]
    }