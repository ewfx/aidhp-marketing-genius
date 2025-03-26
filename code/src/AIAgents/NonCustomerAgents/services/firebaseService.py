import os
from typing import List, Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseService:
    """
    Service for interacting with Firebase services
    Handles initialization, data retrieval, and storage
    """
    _instance = None
    
    def __new__(cls):
        """
        Singleton pattern implementation
        Ensures only one Firebase app is initialized
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """
        Initialize Firebase Admin SDK
        """
        try:
            firebase_admin.get_app()
        except ValueError:
            cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    def fetch_collection_data(self, 
                               collection_name: str, 
                               field: str = 'Content') -> List[str]:
        """
        Fetch data from a specific Firestore collection
        
        Args:
            collection_name (str): Name of the collection
            field (str, optional): Field to extract
        
        Returns:
            List of extracted field values
        """
        collection_ref = self.db.collection(collection_name)
        docs = collection_ref.stream()
        
        return [
            doc.to_dict().get(field, '') 
            for doc in docs 
            if field in doc.to_dict()
        ]
    
    def store_insights(self, 
                       collection_name: str, 
                       document_id: str, 
                       data: Dict[str, Any]):
        """
        Store insights in a Firestore collection
        
        Args:
            collection_name (str): Target collection
            document_id (str): Document identifier
            data (Dict): Insights to store
        """
        collection_ref = self.db.collection(collection_name)
        
        # Add server timestamp
        data['generated_at'] = firestore.SERVER_TIMESTAMP
        
        collection_ref.document(document_id).set({
            'trend_summary': data.get('trendSummary', ''),
            'consumer_insights': data.get('keyConsumerInsights', []) or data.get('consumerInsights', []),
            'market_implications': data.get('marketImplications', []),
            'recommendations': data.get('actionableRecommendations', []),
            'instagram_ad': data.get('instagram_ad', '') or data.get('instagramAd', ''),
            'meta_ad': data.get('meta_ad', '') or data.get('metaAd', ''),
            'linkedin_ad': data.get('linkedin_ad', '') or data.get('linkedinAd', ''),
            'trend_image_url': data.get('trend_image_url', '') or data.get('trendImageUrl', ''),
            'generated_at': firestore.SERVER_TIMESTAMP
        })