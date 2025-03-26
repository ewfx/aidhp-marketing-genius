import pytest
from src.backend.InsightsandRecommendation.app.InsightGenerator.AnalyzeLifeStage import analyze_life_stage
from src.backend.InsightsandRecommendation.app.InsightGenerator.AnalyzeRetentionRisk import analyze_retention_risk
from src.backend.InsightsandRecommendation.app.InsightGenerator.DetectLifeEvents import detect_life_events
from src.backend.InsightsandRecommendation.app.InsightGenerator.DetectRepeatingPatterns import detect_repeating_patterns

@pytest.fixture
def sample_customer_data():
    return {
        'customer_info': {
            'age': 35,
            'marital_status': 'married',
            'occupation': 'software_engineer',
            'income_range': '75000-100000'
        },
        'transactions': [
            {'date': '2024-01-01', 'amount': 1500, 'category': 'rent'},
            {'date': '2024-01-15', 'amount': 500, 'category': 'groceries'},
            {'date': '2024-02-01', 'amount': 1500, 'category': 'rent'},
            {'date': '2024-02-15', 'amount': 450, 'category': 'groceries'}
        ]
    }

def test_analyze_life_stage(sample_customer_data):
    """Test the life stage analysis functionality"""
    result = analyze_life_stage(sample_customer_data)
    assert isinstance(result, dict)
    assert 'primary_life_stage' in result
    assert 'confidence_level' in result
    assert 'key_indicators' in result
    assert 'reasoning' in result

def test_analyze_retention_risk(sample_customer_data):
    """Test the retention risk analysis functionality"""
    result = analyze_retention_risk(sample_customer_data)
    assert isinstance(result, dict)
    assert 'risk_level' in result
    assert 'risk_factors' in result
    assert 'recommendations' in result

def test_detect_life_events(sample_customer_data):
    """Test the life events detection functionality"""
    result = detect_life_events(sample_customer_data)
    assert isinstance(result, dict)
    assert 'detected_events' in result
    assert 'confidence_scores' in result
    assert 'event_dates' in result

def test_detect_repeating_patterns(sample_customer_data):
    """Test the repeating patterns detection functionality"""
    result = detect_repeating_patterns(sample_customer_data)
    assert isinstance(result, dict)
    assert 'patterns' in result
    assert 'pattern_confidence' in result
    assert 'pattern_dates' in result

def test_error_handling():
    """Test error handling with invalid data"""
    invalid_data = {'invalid': 'data'}
    result = analyze_life_stage(invalid_data)
    assert 'error' in result
    assert 'raw_response' in result 