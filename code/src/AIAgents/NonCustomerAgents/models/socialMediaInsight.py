from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field

class SocialMediaInsight(BaseModel):
    """
    Structured model for social media insights
    Provides a consistent schema for insight generation
    """
    trend_summary: str = Field(
        description="Concise summary of key trends", 
        default=""
    )
    consumer_insights: List[str] = Field(
        description="Key insights about consumer behavior", 
        default_factory=list
    )
    market_implications: List[str] = Field(
        description="Potential implications for the market", 
        default_factory=list
    )
    recommendations: List[str] = Field(
        description="Actionable recommendations", 
        default_factory=list
    )
    instagram_ad: Optional[str] = Field(
        description="Instagram ad copy based on trend summary",
        default=None
    )
    meta_ad: Optional[str] = Field(
        description="Meta ad copy based on trend summary", 
        default=None
    )
    linkedin_ad: Optional[str] = Field(
        description="LinkedIn ad copy based on trend summary", 
        default=None
    )
    trend_image_url: Optional[str] = Field(
        description="URL of the generated trend image", 
        default=None
    )
    def to_dict(self):
        """
        Convert the model to a dictionary
        
        Returns:
            Dict representation of the model
        """
        return {
            "trend_summary": self.trend_summary,
            "consumer_insights": self.consumer_insights,
            "market_implications": self.market_implications,
            "recommendations": self.recommendations,
            "instagram_ad": self.instagram_ad,
            "meta_ad": self.meta_ad,
            "linkedin_ad": self.linkedin_ad,
            "trend_image_url": self.trend_image_url
        }