import pandas as pd
from datetime import datetime, timedelta


class DataFetcher:
    def __init__(self, firestore_client, client_id):
        """
        Initialize DataFetcher with Firestore client and client ID

        Args:
            firestore_client (firestore.Client): Firestore client
            client_id (str): Unique identifier for the client
        """
        self.db = firestore_client
        self.client_id = str(client_id)

    def fetch_new_data(self, days=1):
        """
        Fetches data updated in the last N days

        Args:
            days (int): Number of days to look back

        Returns:
            dict: Dictionary containing transaction and app activity data
        """
        transactions_cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        # Fetch new transactions
        transactions = self.db.collection('TransactionData').document(self.client_id) \
            .collection('transactions') \
            .where('Transaction_Date', '>=', transactions_cutoff_date) \
            .stream()

        # Fetch new website interactions
        app_activity = self.db.collection('AppActivity').document(self.client_id).get()

        data = app_activity.to_dict() or {}
        sessions = data.get('sessions', [])

        # Filter sessions by cutoff date
        app_activity_cutoff_date = datetime.now() - timedelta(days=days)
        filtered_sessions = [
            session for session in sessions
            if datetime.fromisoformat(session['date']) >= app_activity_cutoff_date
        ]

        # Convert to pandas dataframes for analysis
        transaction_data = pd.DataFrame([t.to_dict() for t in transactions])
        app_activity_data = pd.DataFrame(filtered_sessions)

        return {
            'transactions': transaction_data,
            'app_activity': app_activity_data
        }

    def fetch_historical_context(self):
        """
        Fetches aggregated historical data and previous insights

        Returns:
            dict: Historical context data for the client
        """
        customer_data_fields = ["life_stage", "life_events", "spending_patterns", "retention_risk"]

        latest_historical_context = {"basic_customer_data": self.db.collection('CustomerData').document(
            self.client_id).get().to_dict()}

        for key in customer_data_fields:
            latest_doc = self.db.collection('CustomerData').document(self.client_id) \
                .collection(key) \
                .order_by('created_at', direction='DESCENDING') \
                .limit(1) \
                .get()

            for doc in latest_doc:
                latest_historical_context[key] = doc.to_dict()

        return latest_historical_context
