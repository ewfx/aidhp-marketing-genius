import praw
import tweepy
import pandas as pd
import datetime
import os
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
        
    
    def search_reddit(self, keyword, limit=10):
        """Search Reddit for posts containing the keyword"""
        print(f"Searching Reddit for: {keyword}")
        
        data = []
        
        # Search in submissions
        for submission in self.reddit.subreddit("all").search(keyword, limit=limit):
            data.append({
                'platform': 'Reddit',
                'type': 'post',
                'id': submission.id,
                'author': str(submission.author),
                'title': submission.title,
                'content': submission.selftext,
                'url': f"https://www.reddit.com{submission.permalink}",
                'created_utc': datetime.datetime.fromtimestamp(submission.created_utc),
                'score': submission.score,
                'num_comments': submission.num_comments
            })
            
            # Get comments from this submission
            submission.comments.replace_more(limit=0)  # Skip "load more comments" items
            for comment in submission.comments.list():
                if keyword.lower() in comment.body.lower():
                    data.append({
                        'platform': 'Reddit',
                        'type': 'comment',
                        'id': comment.id,
                        'author': str(comment.author),
                        'title': submission.title,
                        'content': comment.body,
                        'url': f"https://www.reddit.com{comment.permalink}",
                        'created_utc': datetime.datetime.fromtimestamp(comment.created_utc),
                        'score': comment.score,
                        'parent_id': comment.parent_id
                    })
        
        return data
    
    def perform_search(self, keyword, output_file=None):
        """Perform search across all platforms and return results"""
        all_data = []
        
        # Get data from Reddit
        try:
            reddit_data = self.search_reddit(keyword)
            all_data.extend(reddit_data)
            print(f"Found {len(reddit_data)} Reddit items")
        except Exception as e:
            print(f"Error searching Reddit: {e}")
        
        # # Get data from Twitter
        # try:
        #     twitter_data = self.search_twitter(keyword)
        #     all_data.extend(twitter_data)
        #     print(f"Found {len(twitter_data)} Twitter items")
        # except Exception as e:
        #     print(f"Error searching Twitter: {e}")
            
        # Save to CSV if output file specified
        if output_file and all_data:
            df = pd.DataFrame(all_data)
            df.to_csv(output_file, index=False)
            print(f"Data saved to {output_file}")
            
            # Also save as JSON for unstructured access
            json_file = output_file.replace('.csv', '.json')
            df.to_json(json_file, orient='records')
            print(f"JSON data saved to {json_file}")
        
        return all_data

# Example usage
if __name__ == "__main__":
    listener = SocialListener()
    keyword = input("Enter keyword to search for: ")
    output_file = f"{keyword.replace(' ', '_')}_social_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    results = listener.perform_search(keyword, output_file)
    print(f"Total results found: {len(results)}")