import praw
class Redditscraper:
    def __init__(self, my_client_id, 
                 my_client_secret, 
                 my_user_agent):
        
        self.reddit = praw.Reddit(client_id=my_client_id,
                                  client_secret=my_client_secret,
                                  user_agent=my_user_agent)
        print(self.reddit.read_only)
    
    def scrape_comments(self, commenterID):
        submission = self.reddit.submission(id=commenterID)
        submission.comment_sort="new"
        all_comments = submission.comments.list()

        return all_comments

    def get_single_post(self, post_url):

        post = self.reddit.submission(url=post_url)

        response =  {
            'title': post.title,
            'score': post.score,
            'id': post.id,
            'url': post.url,
            'comments': [comment.body for comment in post.comments]

        }
        
        return response 

    def get_posts(self, subreddit, limit):
        return self.reddit.subreddit(subreddit).hot(limit=limit)

    def get_comments(self, subreddit, limit):
        return self.reddit.subreddit(subreddit).comments(limit=limit)

    def get_subreddits(self, limit):
        return self.reddit.subreddits.popular(limit=limit)

    def get_user(self, username):
        return self.reddit.redditor(username)