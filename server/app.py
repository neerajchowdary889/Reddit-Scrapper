from flask import Flask, request, session, jsonify, send_file
from datetime import datetime
import csv
from RedditScarpper import Redditscraper

app = Flask(__name__)
app.secret_key = "NeerajNeeraj"

def security(fname):
    try:
        with open('api.csv', mode='a', newline='') as csv_file:

            fieldnames = ['timestamp', 'clientAgent', 'clientIP', 'API']
            
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            if csv_file.tell() == 0:
                writer.writeheader()
            
            writer.writerow({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'clientAgent': str(request.headers.get('User-Agent')),
                'clientIP': str(request.environ['REMOTE_ADDR']),
                'API': fname
            })

            csv_file.close()
            
    except Exception as e:
        print(f"Error writing to CSV file: {str(e)}")

    return None

@app.route('/init', methods=['POST'])
def init():
    """
    Flask route that handles a POST request to initialize a session.
    
    Sets session variables for user agent, client ID, and client secret based on the JSON data in the request.
    Prints the values of these variables and returns a success message.
    
    Returns:
        str: Success message indicating that the initialization was successful.
    """

    security('init')
    try:
        session['user_agent'] = "Scraper 1.0 by /u/python_engineer"
        session['client_id'] = request.json.get('client_id')
        session['client_secret'] = request.json.get('client_secret')
        
        print("Initialization successful")

        return 'Initialization successful', 200
    except Exception as e:
        return f'Error: {str(e)}', 500


@app.route('/init/get_post_byurl', methods=['POST'])
def get_post_byurl():
    """
    Retrieves information about a Reddit post based on its URL.

    Returns:
        JSON response containing information about the post.
    """

    security('get_post_byurl')
    try:
        post_url = request.json.get('post_url')
        print(f"Post URL: {post_url}")
        
        reddit_scraper = Redditscraper(my_client_id=session['client_id'], 
                                       my_client_secret=session['client_secret'], 
                                       my_user_agent=session['user_agent'])
        
        post_response = reddit_scraper.get_single_post(post_url=post_url)

        # print(f"Post: {post_response}")
        
        return jsonify(post_response), 200
    except Exception as e:
        return f'Error: {str(e)}', 500
    

@app.route('/init/get_bysubreddit', methods=['POST'])
def get_bysubreddit():
    """
    Retrieves information about a subreddit and ratelimits.

    Returns:
        CSV file containing information about the subreddit.    
    """

    security('get_bysubreddit')
    try:
        subreddit = request.json.get('subreddit')
        limit = request.json.get('limit')
        print(f"Subreddit: {subreddit}")
        
        reddit_scraper = Redditscraper(my_client_id=session['client_id'], 
                                       my_client_secret=session['client_secret'], 
                                       my_user_agent=session['user_agent'])
        
        csv_file_path = reddit_scraper.scrape_subreddit(subreddit_name=subreddit, limit=limit)
        return send_file(csv_file_path, mimetype='text/csv', as_attachment=True), 200
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4005)