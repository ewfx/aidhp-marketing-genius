# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app,credentials, firestore
from reddit import SocialListener
import os
import functions_framework
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Initialize Firebase Admin SDK
cred = credentials.Certificate('hyperpersonalisationapp-firebase-adminsdk-fbsvc-7f9b035690.json')
initialize_app(cred)
db = firestore.client()

@functions_framework.http
def scrape_social_media(request):
    """
    Cloud Function to scrape social media data and log to Firestore SocialData collection
    """
    try:
        # You can make the keyword configurable via request parameters or environment variables
        # keyword = os.getenv('SCRAPE_KEYWORD', 'technology')
        keyword = "Wells Fargo"
        
        # Initialize the Social Listener
        listener = SocialListener()
        
        # Perform search
        scraped_data = listener.perform_search(keyword)
        
        # Prepare data for Firestore
        social_data_collection = db.collection('SocialData')
        
        # Batch write for efficiency
        batch = db.batch()
        
        for item in scraped_data:
            # Create a new document reference
            doc_ref = social_data_collection.document()
            
            # Prepare document data matching the structure you showed
            doc_data = {
                'Content': item.get('content', ''),
                'Date': item.get('created_utc', datetime.now()),
                'Keywords': [keyword],  # You can expand this if needed
                'SocialHandle': item.get('author', ''),
                'Source': item.get('platform', 'Reddit')
            }
            
            # Add any additional fields from the original data
            batch.set(doc_ref, doc_data)
        
        # Commit the batch write
        batch.commit()
        
        return f'Successfully scraped {len(scraped_data)} items for keyword: {keyword}', 200
    
    except Exception as e:
        # Log error to a separate collection
        error_collection = db.collection('ScraperErrors')
        error_collection.add({
            'error_message': str(e),
            'keyword': keyword,
            'timestamp': datetime.now()
        })
        
        return f'Error in scraping: {str(e)}', 500

# For local testing (optional)
if __name__ == '__main__':
    scrape_social_media(None)