import yaml
import json
import requests
import os

my_path = os.path.abspath(os.path.dirname(__file__))

CONFIG_PATH = os.path.join(my_path, "../../config/config.yml")

with open(CONFIG_PATH,"r") as config_file:
	config = yaml.load(config_file)

def post_message(message):
	payload = {'token': config['slack']['slack_token'], 'channel': config['slack']['channel'] , 'text': message, 'username':config['slack']['username']}
	r = requests.post(config['slack']['post_url'], params=payload)
	return r

def read_message():
	payload = {'token': config['slack']['slack_token'], 'channel': config['slack']['channel'] , 'count': '1'}
	r = requests.get(config['slack']['get_url'], params=payload)
	message = r.json()['messages'][0]['text']
	ts = r.json()['messages'][0]['ts']
	data = r.json()['messages'][0]
	if 'user' not in data:
		return False
	return message

def upload_file(file_path):
	print(file_path)
	f = {'file': (file_path, open(file_path, 'rb'), {'Expires':'0'})}
	r = requests.post(url='https://slack.com/api/files.upload', data=
		{'token': config['slack']['slack_token'], 'channels': config['slack']['channel'], 'media': f}, 
		headers={'Accept': 'application/json'}, files=f)
	return r

def get_username(user_id):
	payload = {'token': config['slack']['slack_token'], 'user': user_id}
	r = requests.post(config['slack']['user_info'], params=payload)
	return r.json()['user']['name']