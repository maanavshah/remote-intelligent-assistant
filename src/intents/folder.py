import os
import sys
import yaml
import json
import requests
from slack import post_message
from slack import read_message
from slack import upload_file

command = ""
pref = ""

my_path = os.path.abspath(os.path.dirname(__file__))

COMMAND_PATH = os.path.join(my_path, "../../data/command.json")
FILES_PATH = os.path.join(my_path, "../../utilities/files")

def multiple_paths(path):
	paths = path.split('\n')
	if len(paths) > 1:
		if len(paths) > 20:
				post_message("Too many folder possibilties. Please try another folder.")
				return("Error")
		post_message("I found multiple folder possibilties. Please make your selection\n"+path)
		slctn = read_message()
		while slctn == False:
			slctn = read_message()
			if int(slctn) >= len(paths):
				post_message("Out of range. Please enter again.")
				slctn = False
		path = paths[int(slctn)]
	return path

def construct_command(user_input,label,tokens,mapping,tags):
	sys.path.insert(0, FILES_PATH)
	from home_search import search_home
	with open(COMMAND_PATH,'r') as cmd:
		data = json.load(cmd)
	source = ""
	dest = ""
	name = ""
	pref = data['folder'][mapping]
	if pref == 'mv' or pref == 'cp -r':
		for pos,tag in enumerate(tags):
			if (tag[1] == 'NNP' or tag[1] == 'NN') and tokens[pos-1] == 'from':
				source = multiple_paths(search_home(tag[0],"~"))
				name = tokens[pos-2]
				if(search_home(name,source) == ""):
					command = "Could not locate folder"
					return(command,0)				
			if (tag[1] == 'NNP' or tag[1] == 'NN') and tokens[pos-1] == 'to':
				dest = multiple_paths(search_home(tag[0],"~"))
			if('from' not in tokens and tokens[pos-1] == 'to'):
				name = multiple_paths(search_home(tokens[pos-2],"~"))
				dest = multiple_paths(search_home(tag[0]),"~")
			command = str(pref)+" "+source+"/"+name+" "+dest
		return(command,0)
	if pref == 'mkdir':
		dest = ""
		name = ""
		for pos,tag in enumerate(tags):
			if(tag[1] == 'NNP' or tag[1] == 'NN') and tokens[pos-1] == 'in':
				dest = multiple_paths(search_home(tag[0],"~"))
				if(dest == ""):
					command = "Could not locate folder in home directory"
					return(command,0)
			if(tag[1] == 'NNP' or tag[1] == 'NN') and tokens[pos-1] == 'folder':
				name = tag[0]
			command = str(pref)+" "+dest+"/"+name
		return(command,0)
	if pref == 'rm -rf':
		flag = 0
		for pos,tag in enumerate(tags):
			if (tag[1] == 'NNP' or tag[1] == 'NN') and tokens[pos-1] == 'from':
				flag = 1
				name = tokens[pos-2]
				dest = multiple_paths(search_home(tokens[pos],"~"))
		if flag == 0:
			for pos,tag in enumerate(tags):
				if(tag[1] == 'NNP' or tag[1] == 'NN') and tokens[pos-1] == 'folder':
					name = ""
					dest = multiple_paths(search_home(tag[0],"~"))
		command = str(pref)+" "+dest+"/"+name
		return(command,0)
	if pref == "ls":
		if "contents" in tokens:
			index = tokens.index("contents")
			if "folder" in tokens:
				indx = tokens.index("folder")
				name = tokens[indx+1]
			else:
				name = tokens[index+2]
			folder_path = multiple_paths(search_home(name,"~"))
		command = str(pref)+" "+folder_path
		return(command,0)
	if pref == "find -name":
		index = 0
		indx = 0
		if "folder" in tokens:
			index = tokens.index("folder")
		elif "directory" in tokens:
			index = tokens.index("directory")
		else:
			command = "Invalid Syntax!"
			return(command,0)
		if "in" in tokens:
			indx = tokens.index("in")
			name = tokens[index+1]
			dest = tokens[indx+1]
		else:
			name = tokens[index+1]
			dest= "~"
		#print("Dest = "+multiple_paths(dest))
		folder_path = multiple_paths(search_home(name,multiple_paths(search_home(dest,"~"))))
		command = folder_path
		return(command,0)