from app.AdaptiveAnalyticsEngine.services.customer_insights_updater import CustomerDataUpdater
from app.AdaptiveAnalyticsEngine.services.llm_based_analysis import prepare_llm_context, analyze_with_llm
from app.AdaptiveAnalyticsEngine.services.summarize_data import summarize_data
from AnalyticsConfig.config import DEFAULT_CONFIG
from app.init import db_client
from services.data_fetcher import DataFetcher


class AnalyticsEngine:
    def __init__(self, client_id, config=None):
        """
        Initialize AdaptiveEngine

        Args:
            client_id (str): Unique identifier for the client
            config (dict, optional): Configuration settings. Defaults to None.
        """
        self.client_id = str(client_id)
        self.config = config or DEFAULT_CONFIG

        # Initialize db connection
        self.db = db_client

        # Initialize services
        self.data_fetcher = DataFetcher(self.client_id, self.db)
        self.customer_insights_updater = CustomerDataUpdater(self.db, self.client_id)

    def run_analysis(self, days=30):
        """
        Run comprehensive data on new data and compare with historical context data

        Args:
            days (int, optional): Number of days of data to analyze. Defaults to 1.

        Returns:
            dict: Analysis results including detected changes
        """
        # Fetch new data
        new_data = self.data_fetcher.fetch_new_data(days)

        # Fetch historical context
        historical_context = self.data_fetcher.fetch_historical_context()

        # Get summaries and statistics of new data
        new_data_summaries = summarize_data(new_data)

        # Prepare context for LLM analysis
        llm_context = prepare_llm_context(historical_context, new_data_summaries)

        # Analyze with LLM and generate insights
        insights = analyze_with_llm(llm_context)

        self.customer_insights_updater.update_customer_insights(self.client_id, insights)
