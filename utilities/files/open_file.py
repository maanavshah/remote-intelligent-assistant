import os
import sys

#opening the file using gedit
def find(name, path):
	for root, dirs, files in os.walk(path):
		if name in files:
			print (os.path.abspath(name))
			os.system("gedit "+name)

if __name__ == "__main__":
	find(sys.argv[1],sys.argv[2])
