from app.AdaptiveAnalyticsEngine.services.customer_insights_updater import CustomerDataUpdater
from app.AdaptiveAnalyticsEngine.services.llm_based_analysis import prepare_llm_context, analyze_with_llm
from app.AdaptiveAnalyticsEngine.services.summarize_data import summarize_data
from app.AdaptiveAnalyticsEngine.AnalyticsConfig.config import DEFAULT_CONFIG
from app.init import db_client
from app.AdaptiveAnalyticsEngine.services.data_fetcher import DataFetcher
import logging

# Setup logging
logger = logging.getLogger(__name__)

class AnalyticsEngine:
    def __init__(self, client_id, config=None):
        """
        Initialize AdaptiveEngine

        Args:
            client_id (str): Unique identifier for the client
            config (dict, optional): Configuration settings. Defaults to None.
        """
        try:
            if not client_id:
                raise ValueError("client_id cannot be empty")
                
            self.client_id = str(client_id)
            self.config = config or DEFAULT_CONFIG

            # Initialize db connection
            if not db_client:
                raise ValueError("Database client is not initialized")
            self.db = db_client

            # Initialize services
            try:
                self.data_fetcher = DataFetcher(self.client_id, self.db)
                self.customer_insights_updater = CustomerDataUpdater(self.db, self.client_id)
            except Exception as e:
                logger.error(f"Failed to initialize services: {str(e)}")
                raise

        except Exception as e:
            logger.error(f"Failed to initialize AnalyticsEngine: {str(e)}")
            raise

    def run_analysis(self, days=30):
        """
        Run comprehensive data on new data and compare with historical context data

        Args:
            days (int, optional): Number of days of data to analyze. Defaults to 1.

        Returns:
            dict: Analysis results including detected changes
        """
        try:
            if not isinstance(days, int) or days <= 0:
                raise ValueError("days must be a positive integer")

            # Fetch new data
            try:
                new_data = self.data_fetcher.fetch_new_data(days)
                if not new_data:
                    logger.warning(f"No new data found for the last {days} days")
            except Exception as e:
                logger.error(f"Failed to fetch new data: {str(e)}")
                raise

            # Fetch historical context
            try:
                historical_context = self.data_fetcher.fetch_historical_context()
                if not historical_context:
                    logger.warning("No historical context found")
            except Exception as e:
                logger.error(f"Failed to fetch historical context: {str(e)}")
                raise

            # Get summaries and statistics of new data
            try:
                new_data_summaries = summarize_data(new_data)
                if not new_data_summaries:
                    logger.warning("Failed to generate data summaries")
            except Exception as e:
                logger.error(f"Failed to summarize data: {str(e)}")
                raise

            # Prepare context for LLM analysis
            try:
                llm_context = prepare_llm_context(historical_context, new_data_summaries)
                if not llm_context:
                    logger.warning("Failed to prepare LLM context")
            except Exception as e:
                logger.error(f"Failed to prepare LLM context: {str(e)}")
                raise

            # Analyze with LLM and generate insights
            try:
                insights = analyze_with_llm(llm_context)
                if not insights:
                    logger.warning("Failed to generate insights")
            except Exception as e:
                logger.error(f"Failed to analyze with LLM: {str(e)}")
                raise

            # Update customer insights
            try:
                self.customer_insights_updater.update_customer_insights(self.client_id, insights)
                logger.info(f"Successfully updated insights for client {self.client_id}")
            except Exception as e:
                logger.error(f"Failed to update customer insights: {str(e)}")
                raise

            return insights

        except Exception as e:
            logger.error(f"Failed to run analysis: {str(e)}")
            raise
