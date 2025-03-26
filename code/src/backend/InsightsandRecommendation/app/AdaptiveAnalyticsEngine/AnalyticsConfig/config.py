DEFAULT_CONFIG = {
    'historical_window_days': 90,  # Look back period
    'significance_threshold': 0.3,  # Threshold for detecting meaningful changes
    'analysis_frequency': '15 Days',  # How often to run comprehensive analysis
    'realtime_triggers': ['large_transaction', 'new_product_interaction', 'life_event']
}