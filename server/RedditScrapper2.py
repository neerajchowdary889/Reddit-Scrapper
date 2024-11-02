from redditwarp.client import Client
from redditwarp.models.comment_tree import CommentForest
import json
import time
from mongoservices import (
    Mongo,
    is_valid_mongo_url
)

class Redditscraper:
    def __init__(self, my_client_id, 
                 my_client_secret, 
                 my_user_agent):
        
        self.client = Client(
            client_id=my_client_id,
            client_secret=my_client_secret,
            user_agent=my_user_agent
        )
        self.client.auth.login_application_only()
        print("Logged in successfully")

    def get_single_post(self, post_url):
        # RedditWarp doesn't use direct URLs to fetch posts, need to parse the ID from the URL
        post_id = post_url.split('/')[-3]  # Extract the ID from the URL
        post = self.client.post.pull(id=post_id)

        # Use the CommentForest to get comments in a similar way as PRAW
        comments = post.comments
        response = {
            'title': post.title,
            'score': post.score,
            'id': post.id,
            'url': post.url,
            'description': post.self_text,
            'comments': [comment.body for comment in comments.iter_flat() if not isinstance(comment, CommentForest)]
        }

        return response 
    
    def scrape_subreddit(self, subreddit_name, limit, Mongo_url):
        offline = False

        if not Mongo_url:
            print("Mongo URL not provided, using offline mode")
            offline = True
        elif not is_valid_mongo_url(Mongo_url):
            print("Invalid Mongo URL, using offline mode")
            offline = True
    
        subreddit = self.client.subreddit.get(subreddit_name)
        hot_posts = subreddit.hot(limit=limit)
        json_file_path = rf'../Datasets/{subreddit_name}_post.jsonl'

        num = 0
        for post in hot_posts:
            if ('.jpg' in post.url) or ('.png' in post.url):
                print(".png")
                continue
            try:
                comments = post.comments
                response = {
                    'title': post.title,
                    'score': post.score,
                    'id': post.id,
                    'url': post.url,
                    'description': post.self_text,
                    'comments': [comment.body for comment in comments.iter_flat() if not isinstance(comment, CommentForest)]
                }

                num += 1
                if num % 10 == 0:
                    print(f"Post {num} scraped")

                if not offline:
                    mongo = Mongo(collection=subreddit_name, Mongo_url=Mongo_url)
                    status = mongo.insert(response)
                    if not status:
                        print(f"Error inserting data into MongoDB, Title --> {response['title']} ")

                if offline:
                    with open(json_file_path, 'a') as f:
                        json.dump(response, f)
                        f.write('\n')
            except Exception as e:
                if hasattr(e, 'response') and e.response.status_code == 429:
                    print("Rate limit exceeded... sleep for 10 seconds")
                    time.sleep(10)

        if offline:
            return ('offline', json_file_path)
        else:
            return ('online', "Data uploaded to MongoDB")
    
    def scrape_olderdata(self, userID, limit):
        if not userID:
            print("Error: No userID provided")
            return None
        
        try:
            print(f"Scraping data for user: {userID}")
            user = self.client.user.get(userID)
            submissions = user.get_submissions(limit=limit)
            user_data = []
            for submission in submissions:
                data = {
                    'url': submission.url,
                    'title': submission.title,
                    'description': submission.self_text if submission.is_self else None
                }
                user_data.append(data)
            return user_data
        
        except Exception as e:
            print(e)
            return None
    
    def getId_by_name(self, username):
        try:
            user = self.client.user.get(username)
            return {"UserID": user.id, "FullName": user.name}
        except Exception as e:
            print(e)
            return None
val = Redditscraper("RrNZ7mBHM2Eivu_tjJ5P7w", "jUM3-NjnW3hxFVnTDVNrwJ_5r4TFhw", "my_user_agent")