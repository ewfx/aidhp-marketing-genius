from dotenv import load_dotenv
import time
# Load environment variables
load_dotenv()

# Import specific agents
from agents.creditCardAgent import CreditCardSocialMediaInsightAgent
from agents.homeLoanAgent import HomeLoanSocialMediaInsightAgent
from agents.autoLoanAgent import AutoLoanSocialMediaInsightAgent
from agents.mortgageAgent import MortgageSocialMediaInsightAgent

def main():
    """
    Main execution point for AI agents
    """
    # Create and run Social Media Insight Agent
    credit_card_social_media_agent = CreditCardSocialMediaInsightAgent()
    mortgage_social_media_agent = MortgageSocialMediaInsightAgent()
    auto_loan_social_media_agent = AutoLoanSocialMediaInsightAgent()
    home_loan_social_media_agent = HomeLoanSocialMediaInsightAgent()
    credit_card_social_media_agent.initialize()
    mortgage_social_media_agent.initialize()
    auto_loan_social_media_agent.initialize()
    home_loan_social_media_agent.initialize()
    
    credit_card_social_media_agent.run()
    time.sleep(10)
    mortgage_social_media_agent.run()
    time.sleep(10)
    auto_loan_social_media_agent.run()
    time.sleep(10)
    home_loan_social_media_agent.run()
    time.sleep(10)
    #print("Social Media Insights:", insights)

if __name__ == "__main__":
    main()