import logging
from datetime import datetime
from flask import Blueprint, request
from app.AdaptiveAnalyticsEngine.analytics_engine import AnalyticsEngine
from app.InsightGenerator.AnalyzeLifeStage import analyze_life_stage
from app.InsightGenerator.AnalyzeRetentionRisk import analyze_retention_risk
from app.InsightGenerator.AnalyzeSpendingPattern.AnalyzeSpendingPattern import analyze_spending_patterns
from app.InsightGenerator.DetectLifeEvents import detect_life_events
from app.init import db_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

initial_insight_generation_bp = Blueprint('initial_insight_generation', __name__)


@initial_insight_generation_bp.route('/generate_initial_insights', methods=['POST'])
def generate_initial_insights():
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

            customer_info = customer.to_dict()

            # Fetch transactions associated with a specific client_id
            transactions = db.collection('TransactionData') \
                .document(str(client_id)) \
                .collection('transactions') \
                .stream()
            transactions_list = [transaction.to_dict() for transaction in transactions]

            app_activity = db.collection('AppActivity') \
                .document(str(client_id)) \
                .get()

            # Retrieve the 'sessions' array
            data = app_activity.to_dict()
            sessions = data.get('sessions', [])

            data = {
                "customer_info": customer_info,
                "transactions": transactions_list,
                "app_activity": sessions}

            insights = {}
            insights["life_stage"] = analyze_life_stage(data)
            insights["life_events"] = detect_life_events(data)
            insights["retention_risk"] = analyze_retention_risk(data)
            insights["spending_patterns"] = analyze_spending_patterns(transactions_list)

            for key, value in insights.items():
                value["created_at"] = datetime.now()
                db.collection("CustomerData").document(client_id).collection(key).add(value)

            db.collection("CustomerInsights").document(client_id).set(insights)

        # Log results
        logging.info(f"Analysis completed by analytics_engine at {datetime.now()}")

        # Optional: Further processing or notifications based on analysis results

    except Exception as e:
        logging.error(f"Error in daily analysis: {e}")
