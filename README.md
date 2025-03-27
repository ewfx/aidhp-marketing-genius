# 🚀 Marketing genius

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)
---

## 🎯 Introduction
Our groundbreaking platform represents a transformative approach to financial product personalization, leveraging state-of-the-art artificial intelligence to create a dynamic, intelligent recommendation ecosystem. By integrating advanced multi-agent AI systems, real-time data processing, and sophisticated insight generation, we've developed a solution that goes beyond traditional marketing approaches, offering unprecedented levels of personalization and customer understanding.

## 🎥 Demo
📹 [Video Demo](/artifacts/demo/video/Screen%20Record.mp4) (if applicable)  
![Demo Gif](/artifacts/demo/screenshots/ScreenRecord.gif)

🖼️ Screenshots:

![Dashboard](artifacts/demo/screenshots/Screen1.jpg)
![Pain Points](artifacts/demo/screenshots/Screen2.jpg)
![Social analysis](artifacts/demo/screenshots/screen3.jpg)
![meta Ad](artifacts/demo/screenshots/Screen4.jpg)
![Linkedin Ad](artifacts/demo/screenshots/Screen5.jpg)
![Customer Insights](artifacts/demo/screenshots/Screen6.jpg)
![Email](artifacts/demo/screenshots/screen7.jpg)
![SPush Notification](artifacts/demo/screenshots/Screen8.jpg)
![Sms](artifacts/demo/screenshots/Screen10.jpg)
![Data](artifacts/demo/screenshots/data.jpg)
![zapier agents](artifacts/demo/screenshots/zapier.jpg)

## 💡 Inspiration
We are enthusisastic AI participants who keep a tab on the latest AI developments, both via normal media as well as through hardcore research paper readings.
Hyper-personalization software is something we have attempted to create in the past during a Google hackathon, where we won the first prize in the ecommerce category.
So we though the same is very much applicable in the financial domain. Hence why we decided to do it as we really wanted to challenge ourselves on how we can improve the software
we built last time. Added to that, last time we didn't really experiment with AI agents. But this time the system is completely agentic and throughout the development process we have learnt 
some of the most efficient ways to create agentic flows within a piece of software.

## ⚙️ What It Does
## ✨ Key Features

### 1. Multi-Agent Data Collection & Analysis
- **Comprehensive Data Gathering**
  - Aggregate data from multiple sources including social media, transaction histories, and user interactions
  - Real-time data collection and processing
  - Hourly updates of insights and trends

### 2. Advanced Personalization Engine
- **Intelligent Recommendation System**
  - AI-powered insights for financial products
  - Personalized recommendations for:
    * Credit Cards
    * Home Loans
    * Mortgages
    * Auto Loans
  - Multi-modal personalization leveraging text, image, and voice inputs

### 3. Targeted Marketing Capabilities
- **Adaptive Marketing Channels**
  - Customer Targeting:
    * SMS
    * Phone Notifications
    * Email
  - Non-Customer Targeting:
    * Meta Ads
    * Instagram Ads
    * LinkedIn Ads
- **AI-Generated Content**
  - Multimodal ad creation
  - Sentiment-driven content generation

### 4. Continuous Feedback Analysis
- **Social Media Monitoring**
  - Real-time brand perception analysis
  - Customer pain point identification
  - Sentiment tracking across platforms

### 5. Ethical AI Considerations
- **Responsible AI Principles**
  - Data privacy management
  - Financial compliance integration
  - Consent management
  - Bias detection and mitigation
    
## 🛠️ How We Built It
## 🧠 Overall Architecture

Our platform is built on a microservices-based, event-driven architecture that leverages cutting-edge agentic AI technologies to create a seamless, intelligent recommendation + content generation system.
![System Architecture](/artifacts/arch/HyperPersonalizationArchitecture.png)

## 🔬 Technical Components
[Technical Doc](/artifacts/arch/technicalDocumentation) 
[Presentation](/artifacts/arch/presentation) 
### 1. Data Collection Layer
#### Technologies
- **Zapier**: Automated data integration
- **Firebase**: Real-time data management
- **Firestore**: NoSQL document database

#### Key Implementation
```python
# Sample data collection agent
class DataCollectionAgent:
    def __init__(self, sources):
        self.sources = sources
        self.firestore_client = initialize_firestore()
    
    def collect_social_media_data(self):
        # Aggregate data from multiple social platforms
        pass
    
    def collect_transaction_data(self):
        # Fetch and normalize financial transaction data
        pass
```

### 2. AI-Powered Insight Generation
#### Technologies
- **LangChain**: AI agent framework
- **Gemini**: Large Language Model
- **Firebase Functions**: Serverless compute

#### Trend Discovery Implementation
```python
def discover_financial_trends(collected_data):
    """
    Analyze collected data to generate actionable insights
    
    Args:
        collected_data (dict): Aggregated data from various sources
    
    Returns:
        dict: Processed insights and recommendations
    """
    # Use Gemini for advanced trend analysis
    insights = gemini_model.generate_insights(collected_data)
    
    # Apply LangChain for structured reasoning
    processed_insights = langchain_agent.refine_insights(insights)
    
    return processed_insights
```

### 3. Personalization Engine
#### Multi-Modal Approach
- **Text Processing**: Natural Language Understanding
- **Image Analysis**: Computer Vision
- **Voice Input**: Speech-to-Text Processing

#### Recommendation Generation
```python
class PersonalizationEngine:
    def generate_recommendations(self, user_profile, financial_trends):
        """
        Create hyper-personalized recommendations
        
        Args:
            user_profile (dict): Comprehensive user data
            financial_trends (dict): Current market insights
        
        Returns:
            list: Tailored product recommendations
        """
        # Combine user profile with market trends
        contextual_recommendations = self.ai_model.generate(
            user_profile, 
            financial_trends
        )
        
        return contextual_recommendations
```

### 4. Marketing Automation
#### Multi-Channel Targeting
- **SMS Gateway**: Direct messaging
- **Email Services**: Detailed communications
- **Ad Platform Integrations**: 
  - Meta Ads
  - LinkedIn Ads
  - Instagram Ads

#### Content Generation Agent
```python
def generate_marketing_content(user_segment, recommendation):
    """
    Create personalized marketing content
    
    Args:
        user_segment (str): Target user group
        recommendation (dict): Specific product recommendation
    
    Returns:
        dict: Multimodal marketing content
    """
    # Use Gemini for content generation
    ad_copy = gemini_model.generate_ad_copy(
        user_segment, 
        recommendation
    )
    
    # Generate multimodal content
    content = {
        'text_ad': ad_copy,
        'image_ad': generate_image(ad_copy),
        'targeting_parameters': optimize_targeting(user_segment)
    }
    
    return content
```

### 5. Feedback and Continuous Learning
#### Monitoring Mechanisms
- **Reddit API**: Community sentiment analysis
- **Social Media Scrapers**: Brand perception tracking
- **Sentiment Analysis**: Continuous feedback loop

## 🔒 Ethical AI Considerations

### Privacy and Compliance
- **Data Anonymization**: Remove personally identifiable information
- **Consent Management**: User-controlled data sharing
- **Bias Detection**: Continuous model auditing

### Bias Mitigation Strategy
```python
def detect_recommendation_bias(recommendations):
    """
    Analyze recommendations for potential biases
    
    Args:
        recommendations (list): Generated product suggestions
    
    Returns:
        dict: Bias assessment report
    """
    bias_checks = [
        'demographic_fairness',
        'socioeconomic_representation',
        'product_accessibility'
    ]
    
    bias_report = bias_detection_model.assess(
        recommendations, 
        bias_checks
    )
    
    return bias_report
```

## 🚀 Deployment Strategy
- **Backend**: Python Flask on Google Cloud Run
- **Frontend**: Next.js Frontend deployed on Firebase Hosting
- **Database**: Firebase Firestore

## 🚧 Challenges We Faced
Describe the major technical or non-technical challenges your team encountered.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/aidhp-marketing-genius.git
   ```
2. Install dependencies and run Frontend
   ```sh
   cd aidhp-marketing-genius/code/src/frontend
   npm install
   npm run dev
   ```
   This opens up the forntend on localhost
3. Install dependencies and run backend  
   ```sh
   cd aidhp-marketing-genius/code/src/backend
   pip install -r requirements.txt
   python api.py
   ```
   This runs backend on localhost

## 🏗️ Tech Stack
- 🔹 Frontend: Next.js/Tailwind CSS
- 🔹 Backend: Node.js / Flask / GCP
- 🔹 Database: Firebase Firestore and Firebase Storage
- 🔹 Other: Gemini API/ Vertex Imagen API / Zapier

## 👥 Team
- **Avhijit nair** - [GitHub](https://github.com/Avhijit-Nair) | [LinkedIn](https://www.linkedin.com/in/avhijit007/)
- **Devam Kakoty** - [GitHub](#) | [LinkedIn](https://www.linkedin.com/in/devam-kakoty/)
