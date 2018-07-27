import yaml
import sys
import json
import requests
import os
import signal
from feedback import get_user_feedback

my_path = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(my_path, "../config/config.yml")

with open(CONFIG_PATH,"r") as config_file:
	config = yaml.load(config_file)

def signal_handler(signal, frame):
	print ('Thank You!')
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def read_message():
	payload = {'token': config['slack']['slack_token'], 'channel': config['slack']['channel'] , 'count': '1'}
	r = requests.get(config['slack']['get_url'], params=payload)
	message = r.json()['messages'][0]['text']
	ts = r.json()['messages'][0]['ts']
	data = r.json()['messages'][0]
	if 'user' not in data:
		user = r.json()['messages'][0]['username']
	else:
		user = r.json()['messages'][0]['user']
	return(message,ts,user)

def post_message(message):
	payload = {'token': config['slack']['slack_token'], 'channel': config['slack']['channel'] , 'text': message, 'username':config['slack']['username']}
	r = requests.post(config['slack']['post_url'], params=payload)
	return r

def get_userlist():
	payload = {'token': config['slack']['slack_token'], 'channel': config['slack']['channel'], 'count': '1'}
	r = requests.post(config['slack']['channel_info'], params=payload)
	return r.json()['channel']['members']

def process_messages():
	#print('I am REIA. How may I help?')
	flag = 1;
	prev_ts = 0;
	while flag == 1:
		user_input,ts,user = read_message()
		if(user_input.lower() == "feedback"):
			get_user_feedback()
			continue
		else:
			if prev_ts != ts:
				#if user == config['slack']['user']:
				#print("user = "+user)
				if user in get_userlist():
					print("user = "+user)
					prev_ts = ts
					if user_input.split(' ', 1)[0] == "<@U3LCC7MS4>":
						print(user+" "+user_input.split(' ', 1)[1]+"\n")
						with open("mqueue.txt", "a") as mssg_file:
							mssg_file.write(user+" "+user_input.split(' ', 1)[1]+"\n")

process_messages()