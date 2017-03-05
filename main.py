from flask import Flask, render_template, request, redirect, json, url_for
from connection import APIConnect
from twython import Twython
import time

# Create the flask app
app = Flask(__name__)

# Create a Twitter Connection
api = APIConnect()

# Home Page
@app.route('/')
def main():
	query = 'custserv'
	count = 100
	new_tweets = api.search(q=query, count=count, result_type='recent', include_entities=False)
	return render_template('index.html', response = new_tweets)

# Fetch more tweets when user scrolls to the bottom of the page
@app.route('/getMoreTweets', methods=['GET'])
def getMoreTweets(max_id=None):	
	# Hashtag and max results to be retrieved
	query = 'custserv'
	count = 100

	data = request.args.get('next_results') # data = ?max_id=838419088577814528&q=custserv&count=100&include_entities=1	
	
	# Error Handling : If no parameter passed
	if data == None:
		return json.dumps({ 'status':400,
							'html':'Invalid Request Parameters'
						});;

	fields = data[1:].split('&')

	# Extract max_id from URL
	max_id = filter(lambda x: 'max_id' in x, fields)[0].split('=')[1]

	# Fetch new tweets
	new_tweets = api.search(q=query, count=count, result_type='recent', 
							include_entities=False, max_id=int(max_id))

	# Error Handling
	if new_tweets['statuses']:
		tweets = new_tweets['statuses'];
		html = '';
		
		for tweet in tweets:
			# Skip if the tweet hasn't been retweeted
			if tweet['retweet_count'] == 0:
				continue

			# Format time at which tweet is created
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

		"""
		Store new next_results which contain 
			- max_id
			- query
			- count
			- include_entities
		"""
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

# Jinja custom filter
@app.template_filter('format_datetime')
def _jinja2_filter_format_datetime(date):
	pyDate = time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y') # Convert Twitter Date to Python Date/Time
	return time.strftime('%Y-%m-%d %H:%M:%S', pyDate) # Return formatted date

# Run the app
if __name__ == '__main__':
	app.run(debug=True, port = 5002)
