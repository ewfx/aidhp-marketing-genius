import os
from typing import Dict, Any, Optional,Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import uuid
from utils import GCP_PROJECT_ID
import re
from langchain_core.messages import AIMessage
# Import Firebase Storage
from firebase_admin import storage

vertexai.init(project = GCP_PROJECT_ID ,location = "us-central1")

class LLMService:
    """
    Service for interacting with Language Models
    Supports different model configurations and prompt strategies
    """
    def __init__(self, 
                 model_name: str = "gemini-2.0-flash", 
                 api_key: Optional[str] = None):
        """
        Initialize LLM Service
        
        Args:
            model_name (str): Name of the language model
            api_key (str, optional): API key for the service
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=self.api_key,
            temperature=0.7,
            max_tokens=1024
        )
        self.imageClient = ImageGenerationModel.from_pretrained("imagen-3.0-fast-generate-001")
    
    def generate_response(self, 
                          prompt_template: ChatPromptTemplate, 
                          input_data: Dict[str, Any], 
                          output_parser: Optional[JsonOutputParser] = None):
        """
        Generate a response using the configured language model
        
        Args:
            prompt_template (ChatPromptTemplate): Prompt template
            input_data (Dict): Input data for the prompt
            output_parser (JsonOutputParser, optional): Output parser
        
        Returns:
            Generated response
        """
        # Create the chain
        chain = prompt_template | self.llm
        
        # Add output parser if provided
        if output_parser:
            chain = chain | output_parser
        
        # Generate response
        return chain.invoke(input_data)
    
    def generate_and_upload_imagen_image(self, 
                                          prompt: str,) -> Optional[str]:
        """
        Generate an image using Imagen and upload to Firebase Storage
        
        Args:
            prompt (str): Image generation prompt
            width (int, optional): Image width
            height (int, optional): Image height
        
        Returns:
            str: URL of the uploaded image in Firebase Storage
        """
        try:
            # Generate image with Imagen
            imagen_response = self.imagen_client.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="9:16",
                person_generation="allow_adult",
                safety_filter_level="strict"
            )
            
            # Get the first generated image
            generated_image = imagen_response.images[0]
            
            # Convert image to bytes
            image_bytes = generated_image.tobytes()
            
            # Generate a unique filename
            unique_filename = f"trend_images/{uuid.uuid4()}.png"
            
            # Get Firebase Storage bucket
            bucket = storage.bucket()
            
            # Create a new blob and upload the image
            blob = bucket.blob(unique_filename)
            blob.upload_from_string(
                image_bytes, 
                content_type='image/png'
            )
            
            # Make the blob publicly accessible
            blob.make_public()
            
            # Return the public URL
            return blob.public_url
        
        except Exception as e:
            print(f"Error in image generation and upload: {e}")
            return None
        
    def _clean_ad_content(self, ad_content: Union[str, AIMessage]) -> str:
        """
        Clean and extract text content from ad generation response
        
        Args:
            ad_content (Union[str, AIMessage]): Generated ad content
        
        Returns:
            str: Cleaned ad text with hashtags preserved
        """
        # If it's an AIMessage, extract the content
        if isinstance(ad_content, AIMessage):
            content = ad_content.content
        else:
            content = str(ad_content)
        
        # Remove headers and bold/italic formatting
        content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'(\*{1,2}|_{1,2})', '', content)
        
        # Extract text content with hashtags
        # Look for the first text-heavy section, preferring options with hashtags
        options = content.split('\n\n')
        
        for option in options:
            # Check if option contains text and hashtags
            if re.search(r'#\w+', option) and len(option.strip().split()) > 5:
                # Clean up remaining markdown, but keep hashtags
                cleaned_option = re.sub(r'^\s*[*#-]\s*', '', option).strip()
                return cleaned_option
        
        # Fallback to first option with some text
        for option in options:
            if len(option.strip().split()) > 5:
                return option.strip()
        
        # Ultimate fallback
        return content[:500].strip()