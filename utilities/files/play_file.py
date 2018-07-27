import sys,os,webbrowser
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
           	return os.path.abspath(root+"/"+name)

path=find(sys.argv[1],"/home")

# 1 for display (text files) in terminal, 0 for open
if sys.argv[2] == '1':
	os.system("cat "+path)
else:	
	webbrowser.open(path)


