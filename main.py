from flask import Flask, render_template, request, redirect, json, url_for
from connect import connect
from twython import Twython
import time, os

app = Flask(__name__)

api = connect()

# Home Page
@app.route('/')
def main():

	last_id = -1
	query = 'custserv'
	count = 100
	app.jinja_env.filters['format_datetime'] = format_datetime

	new_tweets = api.search(q=query, count=count, result_type='recent', include_entities=False)

	# #save the id of the oldest tweet less one
	# oldest = alltweets[-1].id - 1

	# print api
	return render_template('index.html', response = new_tweets)

@app.route('/getMoreTweets', methods=['GET'])
def getMoreTweets(max_id=None):
	data = request.args.get('next_results')
	query = 'custserv'
	count = 100
	# data = "?max_id=838419088577814528&q=custserv&count=100&include_entities=1"
	
	fields = data[1:].split('&')
	max_id = filter(lambda x: 'max_id' in x, fields)[0].split('=')[1]
	new_tweets = api.search(q=query, count=count, result_type='recent', include_entities=False, max_id=int(max_id))

	if new_tweets['statuses']:
		tweets = new_tweets['statuses'];
		html = '';
		
		for tweet in tweets:
			if tweet['retweet_count'] == 0:
				continue

			ts = time.strftime('%a %b %d %Y %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

			html += "<div class='timeline-tweets panel panel-default'>";
			html += "<div class='panel-body'>";
			html += "<img src='" + tweet['user']['profile_image_url'] + "' class='img-thumbnail timeline' width='50'>";
			html += "<p><a href='http://twitter.com/intent/user?screen_name=" + tweet['user']['screen_name'] +"' target='_blank'>" + tweet['user']['name'] + " <span class='text-muted'>@" + tweet['user']['screen_name'] + "</span></a></p>";
			html += (tweet['text']) + "<br>";
			html += "<span class='text-muted small'>" + ts + "</span>";
			html += "<p class='tweet-controls' align='right'>";
			html += "<a href='https://twitter.com/intent/tweet?in_reply_to=" + tweet['id_str'] + "' target='_blank'> Reply</a>  |  <a href='https://twitter.com/intent/favorite?tweet_id=" + tweet['id_str'] + "' target='_blank'>Favorite</a>  |  <a href='https://twitter.com/intent/retweet?tweet_id=" + tweet['id_str'] + "' target='_blank'>Retweet</a>";
			html += "</p>";
			html += "</div>";
			html += "</div>";

		new_next_results = new_tweets['search_metadata']['next_results'];

		return json.dumps({ 'status':200,
							'html':html,
							'old_next_results':data,
							'new_next_results':new_next_results
						});
	else:
		return json.dumps({ 'status':400,
							'html':'',
							'old_next_results':data,
							'new_next_results':data
						});

def format_datetime(value):
	ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(value,'%a %b %d %H:%M:%S +0000 %Y'))
	return ts

def connect():
	consumer_key=os.environ.get('CONSUMER_KEY')
	consumer_secret=os.environ.get('CONSUMER_SECRET')
	access_token=os.environ.get('ACCESS_TOKEN')
	access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET')

	api = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
	return api

# Run the app
if __name__ == '__main__':
	app.run(debug=True, port = 5002)
