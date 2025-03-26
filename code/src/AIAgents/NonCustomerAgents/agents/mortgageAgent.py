from typing import Any, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from services.firebaseService import FirebaseService
from services.llmService import LLMService
from models.socialMediaInsight import SocialMediaInsight
import logging
from core.baseAgent import BaseAgent

class MortgageSocialMediaInsightAgent(BaseAgent):
    """
    Specialized agent for generating social media insights about Mortgages
    """
    def __init__(self, 
                 name: str = "MortgageSocialMediaInsightAgent",
                 collection_name: str = "MortgageSocialData"):
        """
        Initialize the Auto Loan Social Media Insight Agent
        
        Args:
            name (str): Agent name
            collection_name (str): Firestore collection to analyze
        """
        super().__init__()
        
        self.firebase_service = FirebaseService()
        self.llm_service = LLMService()
        self.collection_name = collection_name
        self.logger = logging.getLogger(name)
        
        # Prompt template for insight generation
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert social media trend analyst specializing in mortgage usage and experience insights.
            
            Analyze the provided social media conversations with the following objectives:
            1. Identify emerging trends in mortgage usage
            2. Understand consumer sentiments and behaviors
            3. Detect pain points and positive experiences
            4. Provide actionable insights for financial institutions
            
            Provide a structured, comprehensive analysis."""),
            ("human", """Analyze the following social media conversations about mortgage usage:

            Social Media Content:
            {content}

            Generate insights following this structure:
            - Provide a concise trend summary
            - List key consumer insights
            - Outline potential market implications
            - Suggest actionable recommendations for financial service providers
            
            Respond in a structured, JSON-friendly format.""")
        ])
         # Prompt template for ad generation
        self.ad_prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a professional marketing copywriter specializing in creating targeted social media ads."""),
            ("human", """Create a compelling {platform} ad targeting credit card users based on this trend summary:

            Trend Summary: {trend_summary}

            Guidelines:
            - Keep the ad concise and engaging
            - Highlight key benefits or insights
            - Use platform-specific language and tone
            - Include a clear call-to-action
            - Don not include image prompts
                         
            Provide the ad copy in a clear, direct format. Create only one ad content""")
        ])
        
        # Prompt template for image generation
        self.image_prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in generating descriptive prompts for image generation using Imagen."""),
            ("human", """Create a detailed, vivid image generation prompt based on this trend summary:

            Trend Summary: {trend_summary}

            Generate a prompt that:
            - Visually represents the key insights
            - Uses engaging, descriptive language
            - Ensures the image is professional and relevant to credit card trends
            - Provides specific details for Imagen to create a compelling visual""")
        ])
        
        # Output parser
        self.output_parser = JsonOutputParser(pydantic_object=SocialMediaInsight)
    
    def initialize(self):
        """
        Initialize agent resources
        """
        self.log_action('info', 'Initializing Auto Loan Social Media Insight Agent')
    
    def run(self, input_data: Any = None) -> Dict:
        """
        Generate social media insights
        
        Args:
            input_data (Any, optional): Custom input data
        
        Returns:
            Generated insights
        """
        try:
            # Fetch social media content
            content = self.firebase_service.fetch_collection_data(
                self.collection_name
            )
            content_str = " ".join(content)
            
            # Generate insights
            insights = self.llm_service.generate_response(
                prompt_template=self.prompt_template,
                input_data={'content': content_str},
                output_parser=self.output_parser
            )
            # Generate platform-specific ads
            platforms = ['instagram', 'meta', 'linkedin']
            for platform in platforms:
                ad = self.llm_service.generate_response(
                    prompt_template=self.ad_prompt_template,
                    input_data={
                        'platform': platform, 
                        'trend_summary': insights.get('trendSummary')
                    }
                )
                ad = self.llm_service._clean_ad_content(ad)
                # Dynamically set ad based on platform
                if platform == 'instagram':
                    insights['instagram_ad'] = ad
                elif platform == 'meta':
                    insights['meta_ad'] = ad
                else:
                    insights['linkedin_ad'] = ad
            
            # Generate image prompt and use Imagen
            image_prompt = self.llm_service.generate_response(
                prompt_template=self.image_prompt_template,
                input_data={'trend_summary': insights.get('trendSummary')}
            )
            image_prompt = self.llm_service._clean_ad_content(image_prompt)
            print(image_prompt)
             # Generate and upload image using Imagen
            insights['trend_image_url'] = self.llm_service.generate_and_upload_imagen_image(
                prompt=image_prompt
            )
            # Store insights
            self.firebase_service.store_insights(
                collection_name='SocialMediaInsights',
                document_id='Mortgage',
                data=insights
            )
            
            self.log_action('info', 'Insights generated successfully')
            return insights
        
        except Exception as e:
            self.log_action('error', f'Error generating insights: {e}')
            raise