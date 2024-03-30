import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

s = requests.Session()

def init():
    init_url = 'http://127.0.0.1:4005/init'

    data = {
        'client_id': os.environ.get('client_id'),
        'client_secret': os.environ.get('client_secret')
    }

    response = s.post(init_url, json=data)

    if response.status_code == 200:
        print('Initialization successful')
    else:
        print('Error initializing session:', response.text)

def get_post_byurl(post_url): 
    get_post_byurl_url = 'http://127.0.0.1:4005/init/get_post_byurl'

    data = {
        'post_url': post_url
    }

    response = s.post(get_post_byurl_url, json=data)

    if response.status_code == 200:
        print('Post retrieved successfully')
        with open('response.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
    else:
        print('Error retrieving post:', response.text)


def get_bysubreddit(subreddit, limit, Mongo_url):
    get_post_subreddit = 'http://127.0.0.1:4005/init/get_bysubreddit'

    data = {
        'subreddit': subreddit,
        'limit': limit,
        'Mongo_url': Mongo_url
    }

    response = s.post(get_post_subreddit, json=data)

    if response.status_code == 200:
        print('Post retrieved successfully')
        with open(f"{subreddit}_post.jsonl", 'wb') as f:
            f.write(response.content)
    elif response.status_code == 201:
        response = response.json()
        print(response)

    else:
        print('Error retrieving post:', response.text)

def userid_by_name(name):
    url = f"http://127.0.0.1:4005/init/getid_by_name?username={name}"
    response = s.get(url)
    if response.status_code == 200:
        print('UserID retrieved successfully')
        print(f"FullName: {response.json()['FullName']}")
        print(f"UserID: {response.json()['UserID']}")
    else:
        print('Error retrieving post:', response.text)

def get_user_olderPosts(userid, limit):
    get_user_olderPosts_url = 'http://127.0.0.1:4005/init/get_byuser'
    data = {
        'userID': userid,
        'limit': limit
    }
    response = s.post(get_user_olderPosts_url, json=data)
    if response.status_code == 200:
        print('Posts retrieved successfully')
        with open('User_posts_response.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
    else:
        print('Error retrieving post:', response.text)



init()
get_bysubreddit('blockchaindeveloper', 10, None)
# userid_by_name('deshe')
# get_user_olderPosts('deshe', 10)