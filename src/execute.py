import os
import json
import sys
import yaml
import requests
import subprocess

my_path = os.path.abspath(os.path.dirname(__file__))

SLACK_PATH = os.path.join(my_path, "../src/intents")

def construct_command(user_input,label,tokens,mapping,tags,exec_command,user_tag):
	command = ""
	response = 0
	sys.path.insert(0,SLACK_PATH)
	import slack
	if label == 'folder':
		from folder import construct_command
		command,response = construct_command(user_input,label,tokens,mapping,tags)

	if label == 'network':
		from network import construct_command
		command,response = construct_command(user_input,label,tokens,mapping,tags)

	if label == 'file':
		from file import construct_command
		command,response = construct_command(user_input,label,tokens,mapping,tags)

	if label == 'system':
		from system import construct_command
		command,response = construct_command(user_input,label,tokens,mapping,tags)

	if label == 'general':
		from general import construct_command
		command,response = construct_command(user_input,label,tokens,mapping,tags)

	if exec_command == False:
		if response == 0:
			slack.post_message("@"+user_tag+" "+command)
		else:
			slack.post_message(map_val)
	else:
		if(response == 0):
			slack.post_message("Executing command : \n"+command)
		slack.post_message(execute_command(command,response))

def execute_command(command,response):
	proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)  	
	(out, err) = proc.communicate() 	
	result = out.decode("utf-8").strip('\n') 	
	return result[0:1000]