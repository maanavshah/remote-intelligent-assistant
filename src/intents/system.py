import os
import json
import sys
import yaml
import requests

command = ""
pref = ""

my_path = os.path.abspath(os.path.dirname(__file__))
APP_PATH = os.path.join(my_path, "../../utilities/application")
COMMAND_PATH = os.path.join(my_path, "../../data/command.json")

def construct_command(user_input,label,tokens,mapping,tags):
	sys.path.insert(0, APP_PATH)
	from application import start_application
	from application import kill_application
	with open(COMMAND_PATH,'r') as cmd:
		data = json.load(cmd)
	pref = data['system'][mapping]
	if pref == "application":
		name = tokens[tokens.index("application")+1]
		intent = tokens[tokens.index("application")-1]
		start_words = ["launch","start","open","execute"]
		stop_words = ["kill","end","stop","close","terminate"]
		if intent in start_words:
			start_application(name)
		if intent in stop_words:
			kill_application(name)
		return("Done",0)
	command = str(pref)
	return(command,0)