import os
import json
import sys
import yaml
import requests
from nltk.tag import StanfordPOSTagger

my_path = os.path.abspath(os.path.dirname(__file__))

CONFIG_PATH = os.path.join(my_path, "../config/config.yml")
MAPPING_PATH = os.path.join(my_path, "../data/mapping.json")
TRAINDATA_PATH = os.path.join(my_path, "../data/traindata.json")
COMMAND_PATH = os.path.join(my_path, "../../data/command.json")


with open(CONFIG_PATH,"r") as config_file:
	config = yaml.load(config_file)

os.environ['STANFORD_MODELS'] = config['tagger']['path_to_models']

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

def get_user_feedback():
	usr_input = ""
	label = ""
	command = ""
	post_message('Please enter the input that went wrong')
	usr_input = read_message()
	while usr_input == False:
		usr_input = read_message()
	post_message('Please enter the correct label')
	label = read_message()
	while label == False:
		label = read_message()
	post_message('Please enter the correct Linux command')
	command = read_message()
	while command == False:
		command = read_message()
	post_message("Thank You!")
	update_training_data(usr_input,label,command)
	
def update_training_data(usr_input,label,command):
	format_input = ""
	st = StanfordPOSTagger(config['tagger']['model'],path_to_jar=config['tagger']['path'])
	tags = st.tag(usr_input.split())
	print(tags)
	with open(MAPPING_PATH,'r') as data_file:    
		data = json.load(data_file)
		for pos,tag in enumerate(tags):
			if(tag[1] != "NNP"):
				format_input += tag[0]
				format_input += " "
		data[label].append(format_input)
		with open(MAPPING_PATH, "w") as jsonFile:
			jsonFile.write(json.dumps(data, sort_keys=False, indent=4))
	with open(TRAINDATA_PATH,'r') as data_file:
		data = json.load(data_file)
		add_dict = {
			"text" : format_input,
			"label" : label
		}
		data.append(add_dict)
		with open(TRAINDATA_PATH, "w") as jsonFile:
			jsonFile.write(json.dumps(data, sort_keys=False, indent=4))
	with open(COMMAND_PATH,'r') as data_file:
		data = json.load(data_file)
		add_dict = {
			format_input : command
		}
		data[label].update(add_dict)
		with open(COMMAND_PATH,"w") as jsonFile:
			jsonFile.write(json.dumps(data, sort_keys=False, indent=4))
	print('Added')