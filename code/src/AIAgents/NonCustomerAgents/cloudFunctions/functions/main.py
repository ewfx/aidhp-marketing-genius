# functions/index.py
import os
from firebase_functions import https_fn, scheduler_fn
from firebase_admin import initialize_app


# Initialize Firebase app (only once)
initialize_app()

# Import the agents
from agents.creditCardAgent import CreditCardSocialMediaInsightAgent
from agents.homeLoanAgent import HomeLoanSocialMediaInsightAgent
from agents.autoLoanAgent import AutoLoanSocialMediaInsightAgent
from agents.mortgageAgent import MortgageSocialMediaInsightAgent

@scheduler_fn.on_schedule(schedule="every 24 hours")
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
@scheduler_fn.on_schedule(schedule="every 23 hours")
def run_home_loan_social_media_insights(event: scheduler_fn.ScheduledEvent) -> None:
    """
    Firebase Cloud Function to run Credit Card Social Media Insights Agent
    Triggered every 5 hours
    """
    # Initialize the agent
    social_media_agent = HomeLoanSocialMediaInsightAgent()
    social_media_agent.initialize()
    
    try:
        # Run the agent and generate insights
        insights = social_media_agent.run()
        print("Home Loan Social Media Insights Generated:", insights)
    except Exception as e:
        print(f"Error running Home Loan Social Media Insights Agent: {e}")

@scheduler_fn.on_schedule(schedule="every 22 hours")
def run_mortgage_social_media_insights(event: scheduler_fn.ScheduledEvent) -> None:
    """
    Firebase Cloud Function to run Mortgage Social Media Insights Agent
    Triggered every 5 hours
    """
    # Initialize the agent
    social_media_agent = MortgageSocialMediaInsightAgent()
    social_media_agent.initialize()
    
    try:
        # Run the agent and generate insights
        insights = social_media_agent.run()
        print("Mortgage Social Media Insights Generated:", insights)
    except Exception as e:
        print(f"Error running Mortgage Social Media Insights Agent: {e}")

@scheduler_fn.on_schedule(schedule="every 23 hours")
def run_auto_loan_social_media_insights(event: scheduler_fn.ScheduledEvent) -> None:
    """
    Firebase Cloud Function to run Auto Loan Social Media Insights Agent
    Triggered every 5 hours
    """
    # Initialize the agent
    social_media_agent = AutoLoanSocialMediaInsightAgent()
    social_media_agent.initialize()
    
    try:
        # Run the agent and generate insights
        insights = social_media_agent.run()
        print("Auto Loan Social Media Insights Generated:", insights)
    except Exception as e:
        print(f"Error running Auto loan Social Media Insights Agent: {e}")