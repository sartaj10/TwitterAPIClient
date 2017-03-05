import os
from twython import Twython

# Configure Twitter API
def APIConnect():
	consumer_key=os.environ.get('CONSUMER_KEY')
	consumer_secret=os.environ.get('CONSUMER_SECRET')
	access_token=os.environ.get('ACCESS_TOKEN')
	access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET')

	api = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
	return api
