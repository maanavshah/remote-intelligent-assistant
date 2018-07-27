# Remote Intelligent Assistant (REIA)
A Linux based desktop assistant using Machine Learning and Natural Language Processing

This project is published in International Journal of Application or Innovation in Engineering & Management[Volume 6, Issue 8, August 2017, ISSN 2319 - 4847]. (http://www.ijaiem.org/Volume6Issue8/IJAIEM-2017-06-11-14.pdf)

#### Description
Remote Intelligent Assistant (REIA) is a Linux based desktop application. It is an intelligent assistant that allows the user to communicate with Linux machine in natural language. This application bridges the gap between users and Linux CLI. REIA provides a solution to overcome the limitation of accessing any remote machine using natural language. REIA understands English sentences and converts them into a logically and semantically correct sequence of Linux Bash commands. This way we can provide an abstract natural language interface to any underlying operating system. Remote access to the machine running REIA can further simplify the problem of accessing the machine from mobile devices and browsers from any location in the world. This application also includes a natural language interface for CLI and can handle multiple users simultaneously. If it does not understands the user input, it also provides a recommendation system that suggests the user a list of commands, similar to the user input. It also takes account of the performance by logging and calculating the accuracy of the system. We provide a uniform interface of the application and also ease the task of using the command line effectively.

The application consists of a natural language processing and a machine learning engine for processing the text and keywords, structured with the help of a combination of pipelined combined classifiers – Vectorizer, Term Frequency – Inverse Document Frequency (TF-IDF) and OneVsRest classifier. The system also trains to adapt to the user’s language style, in order to deliver better accuracy even with ambiguity in input. REIA is flexible and scalable as we have integrated Slack for communication. It allows multiple members of the team to access the system remotely. The queuing system ensures that the real-time messages from multiple users are handled. The application can be extended to handle voice input as well, further simplifying the user effort and at almost no cost to the system.

Since our application allows communication through natural language, it will also enable even novice Linux users to interact with the system without any prior knowledge of terminal commands. Additionally, the application will easily automate the task of Linux server administrators. 

#### Environment
1. Linux based system
2. Python3
3. Slack

#### Slack Configuration
1. Create a new slack id on https://slack.com/. Choose a url for your team.
2. Generate your slack token from https://get.slack.help/hc/en-us/articles/215770388-Create-and-regenerate-API-tokens.  
   Paste this token in the config file under slack -> slack_token.
3. You can get your user user_id, channel_id from https://api.slack.com/methods by testing the api method calls.  
   Copy these over to slack -> user and slack -> channel.
4. You should now be able to communicate with REIA. For security purposes, don't share the tokens with anyone. 

#### Installation
1. We have added the dependencies in a requirements.txt file. You can install the same by running   
   pip3 install -r requirements.txt
2. Download Stanford POS Tagger from https://nlp.stanford.edu/software/tagger.shtml. Extract the contents to the ~/Downloads
   folder (You can extract it in any directory). Be sure to modify the 'tagger' parameters appropriately in the config    
   file. 
3. Make sure your system has Java installed. If not proceed as give in the link:
   https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04
4. **Open the src/reia.py file, and change the path on line line 97 (cmd, sed) to reflect the path on your own system.**
5. Open two terminal windows. Navigate to the root directory of the project. Run the following commands in the two seperate
   windows:  
     * python3 src/app.py  
     * pyhton3 src/reia.py
   (You can run the commands using sudo for faster response times, but be careful of the commands you type. We have tried our best
   to avoid any commands that can break or mess with the system)
6. The application should display "Starting..." in the reia.py terminal. Now you are all set.
7. Open up the slack channel or mobile app. Type your messages in the channel with the prefix '@reia' (without quotes).  
   eg. @reia what is my ip address
8. You should see a reply posted to the channel.

Note: If the application doesn't run as expected, check the terminal for any error messages. We run the application with a clean install without any additional installations and debugging. Try and solve the error, as we currently do not have the resources to test the application on different environments. If the error still persists, open a new issue or contact me on my email.

Contact:   
shah.maanav.07@gmail.com
aseemraina1996@gmail.com  

**The entire list of commands that our application can handle for now can be found in the /data folder**
