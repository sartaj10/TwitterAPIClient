import twitter
from twython import Twython

def connect():
	consumer_key="8L9PpfCsYB7LEsFWmWQ6RldgT"
	consumer_secret="zW9ah3n9xjnv6axvgYoavAmv0KuvevTTpb4wcE1AvZRxIY3HrY"
	access_token="635834750-vqlNvbLuZY8rE1eiIALAJIgw0Zc3xyKD6DMLuM4Q"
	access_token_secret="3mFntjEgg9jJyXMiRYNP58YQzvRuwi0nTi3qcEpQKozuY"

	twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
	return twitter