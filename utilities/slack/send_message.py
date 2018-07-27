import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
slack_client = SlackClient(SLACK_TOKEN)


def list_channels():
	channels_call = slack_client.api_call("channels.list")
	if channels_call.get('ok'):
		return channels_call['channels']
	return None
	
def send_message(channel_id, message):
	slack_client.api_call(
		"chat.postMessage",
		channel=channel_id,
		text=message,
		username='maanavshah',
		icon_emoji=':robot_face:'
	)

if __name__ == '__main__':
	channels = list_channels()
	if channels:
		print("Channels: ")
		for channel in channels:
			print(channel['name'] + " (" + channel['id'] + ")")
			if channel['name'] == 'general':
				send_message(channel['id'], "Do you copy?")
	else:
		print("Unable to authenticate.")

