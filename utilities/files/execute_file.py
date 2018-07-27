import os
import subprocess

def search_home(search_key):
	proc = subprocess.Popen(["find ~ -name "+search_key], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	result = out.decode("utf-8").strip('\n')
	print('File located at = '+result)
	command = ""
	if(search_key.lower().endswith('.c')):
		command = "gcc "+result+" ; ./a.out"
	elif(search_key.lower().endswith('.cpp')):
		command = "g++ "+result+" ; ./a.out"
	elif(search_key.lower().endswith('.java')):
		name = search_key.rsplit('.', 1)[0]
		command = "javac "+result+" ; java "+name
	elif(search_key.lower().endswith('.py')):
		command = "python3 "+result
	else:
		print('File Type Not Supported')
	#print('Command : '+command)
	proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	result = out.decode("utf-8").strip('\n')
	print('OUTPUT : \n'+result)
	
search_home('hello.java')
