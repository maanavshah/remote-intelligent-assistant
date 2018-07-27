import os
import json
import sys
import yaml
import requests

command = ""
pref = ""

my_path = os.path.abspath(os.path.dirname(__file__))
SEARCH_PATH = os.path.join(my_path, "../../utilities/google")
COMMAND_PATH = os.path.join(my_path, "../../data/command.json")

def construct_command(user_input,label,tokens,mapping,tags):
	sys.path.insert(0, SEARCH_PATH)
	from webpage import open_in_browser
	from gsearch import get_link
	with open(COMMAND_PATH,'r') as cmd:
		data = json.load(cmd)
	pref = mapping
	if pref == "open website":
		link = ""
		stoppers = ["open","site","page","webpage","link","website"]
		for word in tokens:
			if word not in stoppers:
				link = get_link(word)
				open_in_browser(link,"firefox")			
				command = "Opening "+link
		return(command,0)
	if pref == "show me display trending news from":
		open_in_browser('https://trends.google.co.in/trends/',"firefox")
		command = "Displaying trending news"
		return(command,0)
	if pref == "show weather for in":
		search_term = user_input
		link = get_link(search_term)
		open_in_browser(link,"firefox")
		command = "Displaying weather"
		return(command,0)