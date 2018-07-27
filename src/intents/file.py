import os
import sys
import yaml
import json
import requests
import slack
from slack import post_message
from slack import read_message
from slack import upload_file

command = ""
pref = ""

my_path = os.path.abspath(os.path.dirname(__file__))
FILES_PATH = os.path.join(my_path, "../../utilities/files")
COMMAND_PATH = os.path.join(my_path, "../../data/command.json")

def multiple_paths(path):
	paths = path.split('\n')
	#print("path = "+path)
	if path == "":
		return False
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
	pref = data['file'][mapping]
	name = ""
	source = ""
	dest = ""
	command = ""
	if pref == 'file content':
		flag = 0
		late_stoppers = ["contents","content","data"]	# show/display/view/open/play contents/content/data of file FILE (in/from FOLDER) 
		for word in late_stoppers:
			if word in tokens:
				if(len(tokens) > 5):
					if(tokens[5]=='from' or tokens[5]=='in'):
						dest = multiple_paths(search_home(tokens[6],"~"))
						source = multiple_paths(search_home(tokens[4],dest))
				else:
					name = tokens[4]
					source = multiple_paths(search_home(name,"~"))
				flag = 1
		if not flag:		
			stoppers = ["open","view","play","show","display"] # show/display/open/view/play file FILE
			for word in stoppers:
				if word in tokens:
					name = tokens[tokens.index(word)+2]
					if "in" in tokens:
						dest = multiple_paths(search_home(tokens[tokens.index(word)+4],"~"))
						if dest:
							source = multiple_paths(search_home(name,dest))
					else:
						source = multiple_paths(search_home(name,"~"))
		if(source == False or name == False or dest == False):
			return("Could not locate file or folder!",0)
		else:
			slack.upload_file(source)
		return("Upload success",0)
	if pref == 'rm -rf':
		flag = 0
		for pos,tag in enumerate(tags):				# remove/delete file FILE from/in FOLDER 
			if (tag[1] == 'NNP' or tag[1] == 'NN') and tokens[pos-1] == 'from':
				flag = 1
				name = tokens[pos-2]
				dest = multiple_paths(search_home(tokens[pos],"~"))
		if flag == 0:
			for pos,tag in enumerate(tags):			# remove/delete file FILE
				if(tag[1] == 'NNP' or tag[1] == 'NN') and tokens[pos-1] == 'file':
					name = ""
					dest = multiple_paths(search_home(tag[0],"~"))
		if(dest == False):
			return("Could not locate file or folder!",0)
		else:
			command = str(pref)+" "+dest
		return(command,0) 
	if pref == 'mv' or pref == 'cp -f':
		for pos,tag in enumerate(tags):
			if (tag[1] == 'TO' and pos == 3):		# move/copy file FILE to FOLDER
				src = multiple_paths(search_home(tokens[pos-1],"~"))
				dest = multiple_paths(search_home(tokens[pos+1],"~"))
				if(src == False or dest == False):
					return("Could not locate file or folder!",0)
				else:
					command = str(pref)+" "+src+" "+dest
		for pos,tag in enumerate(tags):
			if (tag[1] == 'IN' and pos == 3):		# move/copy file FILE from FOLDER to FOLDER
				src = multiple_paths(search_home(tokens[pos+1],"~"))
				dest = multiple_paths(search_home(tokens[pos+3],"~"))
				if(dest == False or src == False):
					return("Could not locate file or folder!",0)
				else:
					command = str(pref)+" "+src+"/"+tokens[2]+" "+dest+"/"+tokens[2]
		return(command,0)
	if pref == 'rename mv':
		for pos,tag in enumerate(tags):
			if (tag[1] == 'TO' and pos == 3):		# rename file FILE to FILE
				src = multiple_paths(search_home(tokens[pos-1],"~"))
				if(src == False):
					return("Could not locate file or folder!",0)
				else:
					command = "mv "+src+" "+os.path.abspath(os.path.join(src, os.pardir))+"/"+tokens[4]
					return(command,0)
		for pos,tag in enumerate(tags):
			print(tag,pos)
			if ((tag[1] == 'IN' or tag[1] == 'TO') and pos == 3):		# rename file FILE from/in FOLDER to FILE
				src = multiple_paths(search_home(tokens[pos+1],"~"))
				if(src == False):
					return("Could not locate file or folder!",0)
				else:	
					command = "mv "+src+"/"+tokens[pos-1]+" "+src+"/"+tokens[6]
					return(command,0)
