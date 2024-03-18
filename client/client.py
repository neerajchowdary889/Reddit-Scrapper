import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

s = requests.Session()

init_url = 'http://127.0.0.1:4005/init'

data = {
    'client_id': os.environ.get('client_id'),
    'client_secret': os.environ.get('client_secret')
}

# Send a POST request to the /init route
response = s.post(init_url, json=data)

if response.status_code == 200:
    print('Initialization successful')
else:
    print('Error initializing session:', response.text)

get_post_byurl_url = 'http://127.0.0.1:4005/init/get_post_byurl'

# Define the data to send in the request body
data = {
    'post_url': 'https://www.reddit.com/r/IndianStockMarket/comments/1bhikze/guys_today_i_invested_first_time_in_fo/'
}

response = s.post(get_post_byurl_url, json=data)

if response.status_code == 200:
    print('Post retrieved successfully')
    with open('response.json', 'w') as f:
        json.dump(response.json(), f, indent=4)
else:
    print('Error retrieving post:', response.text)