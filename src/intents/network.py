import os
import sys
import yaml
import json
import requests

command = ""
pref = ""

my_path = os.path.abspath(os.path.dirname(__file__))
FILES_PATH = os.path.join(my_path, "../../utilities/files")
COMMAND_PATH = os.path.join(my_path, "../../data/command.json")
GOOGLE_PATH = os.path.join(my_path, "../../utilities/google")

def construct_command(user_input,label,tokens,mapping,tags):
	sys.path.insert(0, FILES_PATH)
	from home_search import search_home
	with open(COMMAND_PATH,'r') as cmd:
		data = json.load(cmd)
	pref = data['network'][mapping]
	if pref == 'ifconfig':
		command = "ifconfig"
		return(command,0)
	if pref == 'google':
		search_term = ""
		stoppers = ["google","for","web","search","on"]
		for word in tokens:
			if word not in stoppers:
				sys.path.insert(0, GOOGLE_PATH)
				from gsearch import call_search
				search_term += word+" "
				search_result = call_search(search_term)
				command = search_result
		return(command,0)