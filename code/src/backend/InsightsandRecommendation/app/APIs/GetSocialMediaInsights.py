from flask import jsonify, Blueprint
from app.init import db_client
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

social_media_insights_bp = Blueprint('social_media_insights', __name__)


@social_media_insights_bp.route('/get-scoialmediainsights', methods=['GET'])
def get_consumer_insights():
    try:
        # Initialize db connection
        db = db_client
        # Assuming you want to fetch a specific document
        doc_ref = db.collection('SocialMediaInsights')
        docs = doc_ref.stream()
        
        products = []
        for doc in docs:
            product = doc.to_dict()
            # Add document ID if needed
            product['id'] = doc.id
            products.append(product)
        
        return jsonify(products), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


