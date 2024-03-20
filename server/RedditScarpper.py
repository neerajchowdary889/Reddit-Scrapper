import praw
from csv import DictWriter

class Redditscraper:
    def __init__(self, my_client_id, 
                 my_client_secret, 
                 my_user_agent):
        
        self.reddit = praw.Reddit(client_id=my_client_id,
                                  client_secret=my_client_secret,
                                  user_agent=my_user_agent)
        print(self.reddit.read_only)

    def get_single_post(self, post_url):

        post = self.reddit.submission(url=post_url)

        response =  {
            'title': post.title,
            'score': post.score,
            'id': post.id,
            'url': post.url,
            'description': post.selftext,
            'comments': [comment.body for comment in post.comments]

        }
        
        return response 
    
    def scrape_subreddit(self, subreddit_name, limit):
        subreddit = self.reddit.subreddit(subreddit_name)
        hot_posts = subreddit.hot(limit=limit)
        csv_file_path = rf'../Datasets/{subreddit_name}_post.csv'

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
            headers = ['title', 'score', 'id', 'url', 'description', 'comments']
            writer = DictWriter(file, fieldnames=headers)
            writer.writeheader()
            num = 0
            for post in hot_posts:
                post.comments.replace_more(limit=None)
                response = {
                    'title': post.title,
                    'score': post.score,
                    'id': post.id,
                    'url': post.url,
                    'description': post.selftext,
                    'comments':[comment.body for comment in post.comments if not isinstance(comment, praw.models.MoreComments)]
                }
                num += 1
                if num % 10 == 0:
                    print(f"Post {num} scraped")
                writer.writerow(response)

        return csv_file_path