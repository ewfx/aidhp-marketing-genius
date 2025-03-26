from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import specific agents
#from agents.creditCardAgent import CreditCardSocialMediaInsightAgent
#from agents.homeLoanAgent import HomeLoanSocialMediaInsightAgent
from agents.autoLoanAgent import AutoLoanSocialMediaInsightAgent

def main():
    """
    Main execution point for AI agents
    """
    # Create and run Social Media Insight Agent
    #social_media_agent = CreditCardSocialMediaInsightAgent()
    social_media_agent = AutoLoanSocialMediaInsightAgent()
    social_media_agent.initialize()
    
    insights = social_media_agent.run()
    print("Social Media Insights:", insights)

if __name__ == "__main__":
    main()