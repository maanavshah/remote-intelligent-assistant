import os
import subprocess

def start_application (app_name):
	expect = '/usr/bin/'+app_name
	proc = subprocess.Popen(["find /usr/bin -name "+app_name], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	result = out.decode("utf-8").strip('\n')
	if expect == result:
		os.system('/usr/bin/./'+app_name)
	else:
		print('Application not found')
		
def kill_application (app_name):
	proc = subprocess.Popen(["pgrep  "+app_name], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	result = out.decode("utf-8").strip('\n')
	os.system('kill '+result)	
