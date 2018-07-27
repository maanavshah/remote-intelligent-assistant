import yaml
import sys
import random
import nltk
import operator
import jellyfish as jf
import json
import requests
import os
import time
import signal
import subprocess
from nltk.tag import StanfordPOSTagger
from textblob.classifiers import NaiveBayesClassifier
from execute import construct_command
from feedback import get_user_feedback
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing

def signal_handler(signal, frame):
	print ('Thank You!')
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

my_path = os.path.abspath(os.path.dirname(__file__))

CONFIG_PATH = os.path.join(my_path, "../config/config.yml")
MAPPING_PATH = os.path.join(my_path, "../data/mapping.json")
TRAINDATA_PATH = os.path.join(my_path, "../data/traindata.txt")
LABEL_PATH = os.path.join(my_path, "../data/")

sys.path.insert(0, LABEL_PATH)
import trainlabel

with open(CONFIG_PATH,"r") as config_file:
	config = yaml.load(config_file)

os.environ['STANFORD_MODELS'] = config['tagger']['path_to_models']

exec_command = config['preferences']['execute']

def get_username(user_id):
	payload = {'token': config['slack']['slack_token'], 'user': user_id}
	r = requests.post(config['slack']['user_info'], params=payload)
	return r.json()['user']['name']

def read_message():
	payload = {'token': config['slack']['slack_token'], 'channel': config['slack']['channel'] , 'count': '1'}
	r = requests.get(config['slack']['get_url'], params=payload)
	message = r.json()['messages'][0]['text']
	ts = r.json()['messages'][0]['ts']
	data = r.json()['messages'][0]
	if 'user' not in data:
		user = r.json()['messages'][0]['username']
	else:
		user = r.json()['messages'][0]['user']
	return(message,ts,user)

def post_message(message):
	payload = {'token': config['slack']['slack_token'], 'channel': config['slack']['channel'] , 'text': message, 'username':config['slack']['username']}
	r = requests.post(config['slack']['post_url'], params=payload)
	return r
	
def classify(text):
	X_train = np.array([line.rstrip('\n') for line in open(TRAINDATA_PATH)])
	y_train_text = trainlabel.y_train_text
	X_test = np.array([text])
	target_names = ['file', 'folder', 'network', 'system', 'general']

	lb = preprocessing.MultiLabelBinarizer()
	Y = lb.fit_transform(y_train_text)

	classifier = Pipeline([
		('vectorizer', CountVectorizer()),
		('tfidf', TfidfTransformer()),
		('clf', OneVsRestClassifier(LinearSVC()))])

	classifier.fit(X_train, Y)
	predicted = classifier.predict(X_test)
	all_labels = lb.inverse_transform(predicted)

	for item, labels in zip(X_test, all_labels):
		return (', '.join(labels))

def suggestions(suggest_list):
	suggest = (sorted(suggest_list,reverse=True)[:5])
	return suggest

def consume_message():
	cmd = "sed -i -e \"1d\" /home/maanav/REIA/mqueue.txt"
	proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)  	
	(out, err) = proc.communicate()

def call_reia():
	while(True):
		max_score = 0.1
		map_val = ""
		with open('/home/maanav/REIA/mqueue.txt', 'r') as f:
			first_line = f.readline()
			while first_line == "":
				time.sleep(1)
				call_reia()
		print('-----------------------')
		user_input = first_line.split(' ', 1)[1]
		user_name = get_username(first_line.split(' ', 1)[0])
		suggest_list = []
		suggest_message = ""
		#prev_ts = ts
		print("\nINPUT = ")
		print(user_input)
		label = classify(user_input)
		if label == "":
			post_message("Sorry, I could not understand. Please rephrase and try again.")
			consume_message()
			continue
		print("Classified as : "+str(label))
		tokens = nltk.word_tokenize(user_input)
		print(tokens)
		st = StanfordPOSTagger(config['tagger']['model'],path_to_jar=config['tagger']['path'])
		stanford_tag = st.tag(user_input.split())
		print("Tags")
		print(stanford_tag)
		with open(MAPPING_PATH,'r') as data_file:    
			data = json.load(data_file)	
		for i in data[label]:
			dist = jf.jaro_distance(str(user_input),str(i))
			suggest_list.append(tuple((dist,i)))
			print(dist)
			if(dist > max_score):
				max_score = dist
				map_val = i
		if max_score < config['preferences']['similarity_threshold']:
			post_message("Sorry, I could not understand. Please rephrase and try again.")
			consume_message()
			if config['preferences']['suggestions'] == True:
				suggest = suggestions(suggest_list)
				post_message("Did you mean :")
				for i in suggest:
					suggest_message += (str(i[1])+"\n")
				post_message(suggest_message)
			continue
		print("\nMapped to : "+map_val)
		#post_message(map_val)
		construct_command(user_input,label,tokens,map_val,stanford_tag,exec_command,user_name)
		#call('sed -i -e "1d	" REIA/mqueue.txt')
		consume_message()
		#print(response)

print("Starting...")	
call_reia()

