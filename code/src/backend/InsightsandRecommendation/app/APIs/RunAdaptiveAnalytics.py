import logging
from datetime import datetime
from flask import Blueprint, request
from app.AdaptiveAnalyticsEngine.analytics_engine import AnalyticsEngine
from app.init import db_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

run_adaptive_analytics_bp = Blueprint('run_adaptive_analytics', __name__)


@run_adaptive_analytics_bp.route('/run_adaptive_analytics', methods=['POST'])
def run_adaptive_analytics():
    """
        Run the adaptive analytics engine to analyse new data
        """
    try:
        # Initialize db connection
        db = db_client
        customers = None
        if customers is None:
            # Get all active customers
            customers = db.collection('CustomerData').stream()

        for customer in customers:
            client_id = customer.id
            engine = AnalyticsEngine(client_id)
            result = engine.run_analysis()
            logging.info(f"Processed customer {client_id}, detected {len(result['changes_detected'])} changes")

        # Log results
        logging.info(f"Analysis completed by analytics_engine at {datetime.now()}")

        # Optional: Further processing or notifications based on analysis results

    except Exception as e:
        logging.error(f"Error in daily analysis: {e}")
