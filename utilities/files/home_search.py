import os 
import subprocess 

def search_home(search_key,search_path): 	
	#proc = subprocess.Popen(["find ~ -iname "+search_key], stdout=subprocess.PIPE, shell=True)
	proc = subprocess.Popen(["find "+search_path+" -iname "+search_key], stdout=subprocess.PIPE, shell=True)  	
	(out, err) = proc.communicate() 	
	result = out.decode("utf-8").strip('\n') 	
	return result 	

#search_home('slack')

