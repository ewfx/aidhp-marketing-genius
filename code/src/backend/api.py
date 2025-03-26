from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    load_dotenv()  # take environment variables
except Exception as e:
    logger.error(f"Failed to load environment variables: {str(e)}")
    raise

# Initialize Flask app
app = Flask(__name__)
CORS(app)

try:
    # Initialize Firestore
    cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    logger.error(f"Failed to initialize Firebase: {str(e)}")
    raise

@app.route('/get-scoialmediainsights', methods=['GET'])
def get_consumer_insights():
    try:
        # Assuming you want to fetch a specific document
        doc_ref = db.collection('SocialMediaInsights')
        docs = doc_ref.stream()
        
        products = []
        for doc in docs:
            try:
                product = doc.to_dict()
                # Add document ID if needed
                product['id'] = doc.id
                products.append(product)
            except Exception as e:
                logger.error(f"Error processing document {doc.id}: {str(e)}")
                continue
        
        return jsonify(products), 200
    
    except Exception as e:
        logger.error(f"Error fetching social media insights: {str(e)}")
        return jsonify({
            'error': str(e),
            'message': 'Failed to fetch social media insights'
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        logger.error(f"Failed to start Flask application: {str(e)}")
        raise 