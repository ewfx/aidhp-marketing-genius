class CustomerDataUpdater:
    def __init__(self, client_id, firestore_client):
        """
        Initialize CustomerDataUpdater with Firestore client

        Args:
            firestore_client (firestore.Client): Firestore client
        """
        self.db = firestore_client
        self.client_id = client_id

    def update_customer_insights(self, old_insights, llm_analysis):
        """
        Update customer insights based on LLM analysis.

        Args:
        - old_insights (dict): Existing customer insights with keys
          ['spending_pattern', 'retention_risk', 'life_stage', 'life_event']
        - llm_analysis (dict): JSON response from Gemini analysis

        Returns:
        - dict: Updated customer insights, or None if no changes detected
        """
        # Validate input
        if not isinstance(old_insights, dict) or not isinstance(llm_analysis, dict):
            raise ValueError("Inputs must be dictionaries")

        # Map LLM analysis to Firestore keys
        analysis_to_firestore_map = {
            "Spending Patterns": "spending_pattern",
            "Retention Risk": "retention_risk",
            "Life Stage": "life_stage",
            "Life Events": "life_event"
        }
        if llm_analysis["total_changes_detected"] < 1:
            return None

        # Track if any changes occurred
        insights_changed = False
        updated_insights = old_insights.copy()

        # Check each changed metric in the LLM analysis
        if (llm_analysis.get('profile_change_summary', {})
                .get('changed_metrics', [])):

            for metric in llm_analysis['profile_change_summary']['changed_metrics']:
                # Directly check if the metric name matches an existing insight key
                if metric['metric_name'] in old_insights and \
                        metric['new_value'] != old_insights.get(metric['metric_name']):
                    updated_insights[metric['metric_name']] = metric['new_value']
                    insights_changed = True

        # Return updated insights only if changes occurred
        if insights_changed:
            # Create a new document with updated insights
            customer_ref = self.db.collection('CustomerInsights').document(self.client_id)
            customer_ref.set(updated_insights, merge=False)
