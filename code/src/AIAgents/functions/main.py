# functions/index.py
import os
from firebase_functions import https_fn, scheduler_fn
from firebase_admin import initialize_app

# Initialize Firebase app (only once)
initialize_app()

# Import the agents
from agents.creditCardAgent import CreditCardSocialMediaInsightAgent


@scheduler_fn.on_schedule(schedule="every 5 hours")
def run_credit_card_social_media_insights(event: scheduler_fn.ScheduledEvent) -> None:
    """
    Firebase Cloud Function to run Credit Card Social Media Insights Agent
    Triggered every 5 hours
    """
    # Initialize the agent
    social_media_agent = CreditCardSocialMediaInsightAgent()
    social_media_agent.initialize()
    
    try:
        # Run the agent and generate insights
        insights = social_media_agent.run()
        print("Credit Card Social Media Insights Generated:", insights)
    except Exception as e:
        print(f"Error running Credit Card Social Media Insights Agent: {e}")

# You can add more agents here similarly
@scheduler_fn.on_schedule(schedule="every 5 hours")
def run_another_agent(event: scheduler_fn.ScheduledEvent) -> None:
    """
    Placeholder for additional agents
    """
    # Add more agents here as needed
    pass