import json
import time
import logging
from config import Config
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import DeadlineExceeded, ResourceExhausted
from app.utils import GeminiResponseEditor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    load_dotenv()
except Exception as e:
    logger.error(f"Failed to load environment variables: {str(e)}")
    raise

def generate_content(prompt, system_instruction=" ", json_response=False, generation_config=None):
    """
    Generate content using the Gemini API with retry logic and error handling.
    
    Args:
        prompt (str): The input prompt for content generation
        system_instruction (str): System instructions for the model
        json_response (bool): Whether to expect JSON response
        generation_config (dict): Additional configuration for generation
        
    Returns:
        str: Generated content or None if all attempts fail
    """
    try:
        if not prompt:
            raise ValueError("Prompt cannot be empty")
            
        if generation_config is None:
            generation_config = {}
            
        try:
            GEMINI_API_KEY = Config.GEMINI_API_KEY
            if not GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is not set")
            genai.configure(api_key=GEMINI_API_KEY)
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {str(e)}")
            raise

        GENERATION_CONFIG = {
            "temperature": 1,
            #"top_p": 0.95,
            #"top_k": 0,
        }
        if json_response:
            GENERATION_CONFIG["response_mime_type"] = "application/json"

        combined_generation_config = GENERATION_CONFIG | generation_config
        SAFETY_SETTINGS = [
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]

        try:
            model = genai.GenerativeModel(
                "models/gemini-1.5-pro-latest",
                system_instruction=system_instruction,
                generation_config=combined_generation_config,
                safety_settings=SAFETY_SETTINGS,
            )
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            raise

        max_attempts = 3
        last_error = None
        
        for attempt in range(max_attempts):
            try:
                response = model.generate_content(prompt)
                if not response or not response.text:
                    raise ValueError("Empty response from Gemini API")
                    
                formatted_text = GeminiResponseEditor.remove_special_chars(response.text)
                return formatted_text
                
            except DeadlineExceeded as e:
                last_error = e
                logger.warning(f"Deadline exceeded (attempt {attempt + 1}/{max_attempts}). Retrying in 1 second...")
                time.sleep(1)
                
            except json.JSONDecodeError as e:
                last_error = e
                logger.warning(f"JSON decode error (attempt {attempt + 1}/{max_attempts}). Retrying in 1 second...")
                time.sleep(1)
                
            except ResourceExhausted as e:
                last_error = e
                logger.warning(f"Resource exhausted (attempt {attempt + 1}/{max_attempts}). Retrying in 10 seconds...")
                time.sleep(10)
                
            except ValueError as e:
                last_error = e
                if response is not None:
                    logger.warning(f"Value error details: {response.prompt_feedback}")
                    logger.warning(f"Finish reason: {response.candidates[0].finish_reason}")
                    logger.warning(f"Safety ratings: {response.candidates[0].safety_ratings}")
                time.sleep(1)
                
            except Exception as e:
                last_error = e
                logger.error(f"Unexpected error during content generation: {str(e)}")
                time.sleep(1)

        # If all retries fail
        error_msg = f"Failed to generate content after {max_attempts} attempts. Last error: {str(last_error)}"
        logger.error(error_msg)
        return None

    except Exception as e:
        logger.error(f"Critical error in generate_content: {str(e)}")
        raise
