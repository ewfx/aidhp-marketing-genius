import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Add the directory containing main.py to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the SocialListener from main.py
from reddit_phrase_search import SocialListener

def local_scrape_and_log():
    """
    Local function to test scraping and Firestore logging
    """
    try:
        # Initialize Firebase Admin SDK for local testing
        if not firebase_admin._apps:
            # Use service account for local testing
            cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
        os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8080/firestore"
        # Get Firestore client
        db = firestore.client()
        
        # Get keyword from environment
        keyword = os.getenv('SCRAPE_KEYWORD')
        
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
            
            # Prepare document data 
            doc_data = {
                'Content': item.get('content', ''),
                'Date': item.get('date', datetime.now()),
                'Keywords': [],
                'SocialHandle': item.get('author', ''),
                'Source': item.get('source', 'Reddit')
            }
            
            # Add document to batch
            batch.set(doc_ref, doc_data)
        
        # Commit the batch write
        batch.commit()
        
        print(f'Successfully scraped {len(scraped_data)} items for keyword: {keyword}')
        return scraped_data
    
    except Exception as e:
        print(f'Error in local scraping: {str(e)}')
        return None

# Run the local test
if __name__ == '__main__':
    local_scrape_and_log()