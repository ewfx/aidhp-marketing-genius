import os
from typing import List, Dict
import firebase_admin
from firebase_admin import credentials, firestore,initialize_app
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class SocialMediaInsight(BaseModel):
    """Structured output for social media insights"""
    trend_summary: str = Field(description="Concise summary of key trends")
    consumer_insights: List[str] = Field(description="Key consumer insights")
    market_implications: List[str] = Field(description="Potential market implications")
    recommendations: List[str] = Field(description="Actionable recommendations")

class SocialMediaInsightGenerator:
    def __init__(self):
        # Initialize Firebase Admin SDK
        try:
            firebase_admin.get_app()
        except ValueError:
            cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            cred = credentials.Certificate(cred_path)
            initialize_app(cred)
        
        # Initialize Firestore client
        self.db = firestore.client()
        
        # Initialize Langchain Google AI Model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            temperature=0.7,
            max_tokens=None,
        )

    def fetch_social_media_content(self) -> str:
        """
        Fetch all social media content from Firestore
        
        Returns:
            str: Concatenated social media content
        """
        social_data_collection = self.db.collection('CreditCardSocialData')
        
        # Retrieve all documents
        docs = social_data_collection.stream()
        
        # Compile all content into a single string
        all_content = []
        for doc in docs:
            doc_dict = doc.to_dict()
            content = doc_dict.get('Content', '')
            all_content.append(content)
        
        return " ".join(all_content)

    def generate_insights(self, social_media_content: str) -> Dict:
        """
        Generate insights using Langchain and Gemini
        
        Args:
            social_media_content (str): Concatenated social media content
        
        Returns:
            Dict: Generated insights
        """
        # Create a prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert social media trend analyst specializing in credit card usage insights.
            
            Analyze the provided social media conversations with the following objectives:
            1. Identify emerging trends in credit card usage
            2. Understand consumer sentiments and behaviors
            3. Detect pain points and positive experiences
            4. Provide actionable insights for financial institutions
            
            Provide a structured, comprehensive analysis."""),
            ("human", """Analyze the following social media conversations about credit card usage:

            Social Media Content:
            {content}

            Generate insights following this structure:
            - Provide a concise trend summary
            - List key consumer insights
            - Outline potential market implications
            - Suggest actionable recommendations for financial service providers
            
            Respond in a structured, JSON-friendly format.""")
        ])

        # Create an output parser
        output_parser = JsonOutputParser(pydantic_object=SocialMediaInsight)

        # Create the chain
        chain = prompt | self.llm | output_parser

        # Generate insights
        try:
            insights = chain.invoke({"content": social_media_content})
            return insights
        except Exception as e:
            print(f"Error generating insights: {e}")
            return {}

    def store_insights(self, insights: Dict):
        """
        Store generated insights in Firestore
        
        Args:
            insights (Dict): Generated insights
        """
        insights_collection = self.db.collection('SocialMediaInsights')
        
        # Store insight in a specific document
        insights_collection.document('CreditCard').set({
            'trend_summary': insights.get('trendSummary', ''),
            'consumer_insights': insights.get('consumerInsights', []),
            'market_implications': insights.get('marketImplications', []),
            'recommendations': insights.get('actionableRecommendations', []),
            'generated_at': firestore.SERVER_TIMESTAMP
        })

    def run_insight_generation(self):
        """
        Main method to run the entire insight generation process
        """
        try:
            # 1. Fetch social media content
            social_media_content = self.fetch_social_media_content()
            
            # 2. Generate insights
            insights = self.generate_insights(social_media_content)
            
            # 3. Store insights
            self.store_insights(insights)
            
            print("Social Media Insight Generation Completed Successfully")
            return insights
        
        except Exception as e:
            print(f"Error in insight generation: {e}")
            return {}

# Scheduled task or main execution
def main():
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Create and run insight generator
    insight_generator = SocialMediaInsightGenerator()
    results = insight_generator.run_insight_generation()
    
    # Print results for verification
    print("Generated Insights:")
    print(results)
# for local testing
if __name__ == "__main__":
    main()