import os
import sys

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
        	#print os.path.abspath(root+"/"+name)
        	return os.path.abspath(root+"/"+name)
if __name__ == "__main__":
	find(sys.argv[1],sys.argv[2])
	
