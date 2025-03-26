import praw
import pandas as pd
import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class SocialListener:
    def __init__(self):
        # Initialize Reddit API
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
    
    def search_reddit_phrase(self, phrase, limit=10):
        """Search Reddit for posts and comments containing the exact phrase"""
        print(f"Searching Reddit for phrase: {phrase}")
        
        data = []
        
        # Search in submissions
        for submission in self.reddit.subreddit("all").search(f'"{phrase}"', limit=limit):
            # Add submission if it matches the phrase
            if phrase.lower() in submission.title.lower() or phrase.lower() in submission.selftext.lower():
                data.append({
                    'content': submission.title + " " + submission.selftext,
                    'source': 'Reddit',
                    'date': datetime.datetime.fromtimestamp(submission.created_utc).isoformat()
                })
            
            # Get comments from this submission
            submission.comments.replace_more(limit=0)  # Skip "load more comments" items
            for comment in submission.comments.list():
                # Add comment if it matches the phrase
                if phrase.lower() in comment.body.lower():
                    data.append({
                        'content': comment.body,
                        'source': 'Reddit',
                        'date': datetime.datetime.fromtimestamp(comment.created_utc).isoformat()
                    })
        
        return data
    
    def perform_search(self, phrase, output_file=None):
        """Perform phrase search on Reddit and optionally save results"""
        try:
            # Perform phrase search
            search_results = self.search_reddit_phrase(phrase)
            
            # Save to JSON if output file specified
            if output_file and search_results:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(search_results, f, ensure_ascii=False, indent=2)
                print(f"Data saved to {output_file}")
            
            return search_results
        
        except Exception as e:
            print(f"Error in search: {e}")
            return []

# Example usage
if __name__ == "__main__":
    listener = SocialListener()
    phrase = input("Enter phrase to search for: ")
    output_file = f"{phrase.replace(' ', '_')}_social_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.json"
    results = listener.perform_search(phrase, output_file)
    print(f"Total results found: {len(results)}")