from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Firestore
cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/get-scoialmediainsights', methods=['GET'])
def get_consumer_insights():
    try:
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

if __name__ == '__main__':
    app.run(debug=True)

