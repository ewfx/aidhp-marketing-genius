import pytest
from unittest.mock import Mock, patch
from src.backend.InsightsandRecommendation.app.AdaptiveAnalyticsEngine.analytics_engine import AnalyticsEngine
from src.backend.InsightsandRecommendation.app.AdaptiveAnalyticsEngine.AnalyticsConfig.config import DEFAULT_CONFIG

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def analytics_engine(mock_db):
    with patch('src.backend.InsightsandRecommendation.app.AdaptiveAnalyticsEngine.analytics_engine.db_client', mock_db):
        engine = AnalyticsEngine(client_id="test_client_123")
        return engine

def test_analytics_engine_initialization(analytics_engine):
    """Test proper initialization of AnalyticsEngine"""
    assert analytics_engine.client_id == "test_client_123"
    assert analytics_engine.config == DEFAULT_CONFIG
    assert analytics_engine.data_fetcher is not None
    assert analytics_engine.customer_insights_updater is not None

def test_run_analysis_with_default_days(analytics_engine):
    """Test run_analysis with default days parameter"""
    # Mock the data fetcher methods
    analytics_engine.data_fetcher.fetch_new_data = Mock(return_value=[{'data': 'test'}])
    analytics_engine.data_fetcher.fetch_historical_context = Mock(return_value=[{'historical': 'data'}])
    
    # Mock the customer insights updater
    analytics_engine.customer_insights_updater.update_customer_insights = Mock()
    
    result = analytics_engine.run_analysis()
    
    # Verify the methods were called with correct parameters
    analytics_engine.data_fetcher.fetch_new_data.assert_called_once_with(30)
    analytics_engine.data_fetcher.fetch_historical_context.assert_called_once()
    analytics_engine.customer_insights_updater.update_customer_insights.assert_called_once()

def test_run_analysis_with_custom_days(analytics_engine):
    """Test run_analysis with custom days parameter"""
    # Mock the data fetcher methods
    analytics_engine.data_fetcher.fetch_new_data = Mock(return_value=[{'data': 'test'}])
    analytics_engine.data_fetcher.fetch_historical_context = Mock(return_value=[{'historical': 'data'}])
    
    # Mock the customer insights updater
    analytics_engine.customer_insights_updater.update_customer_insights = Mock()
    
    result = analytics_engine.run_analysis(days=7)
    
    # Verify the methods were called with correct parameters
    analytics_engine.data_fetcher.fetch_new_data.assert_called_once_with(7)
    analytics_engine.data_fetcher.fetch_historical_context.assert_called_once()
    analytics_engine.customer_insights_updater.update_customer_insights.assert_called_once()

def test_run_analysis_error_handling(analytics_engine):
    """Test error handling in run_analysis"""
    # Mock the data fetcher to raise an exception
    analytics_engine.data_fetcher.fetch_new_data = Mock(side_effect=Exception("Test error"))
    
    with pytest.raises(Exception) as exc_info:
        analytics_engine.run_analysis()
    
    assert str(exc_info.value) == "Test error"

def test_custom_config_initialization():
    """Test AnalyticsEngine initialization with custom config"""
    custom_config = {
        "analysis_days": 15,
        "confidence_threshold": 0.8
    }
    
    engine = AnalyticsEngine(client_id="test_client_123", config=custom_config)
    assert engine.config == custom_config 