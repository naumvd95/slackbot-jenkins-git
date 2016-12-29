# slackbot-jenkins-git
I. first of all https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

II. confgure integration slack-github

https://miracloud.slack.com/apps/new/A0F7YS2SX-github

III. configure curl-query to jenkins job, using token

https://sonnguyen.ws/how-to-trigger-a-jenkins-build-from-slack/

IV. 
#auto-case

1. git add .

2. git commit -v

3. commit_name and key_phrase (in my ex. = trigger-update) in Commit Naming only now! (first raw)

4. enjoy

#manual-case

1. get into chat

2. @bot_name command (in my ex. = update)

3. enjoy

#docker-case

1. create own auth.env file with following vars

#SLACK_BOT_TOKEN=*********
#BOT_NAME=****************
#JENKINS_URL=*************
#JOB_TOKEN=***************

2. install docker-compose

3. run docker-compose up --build

4. use manual/auto cases

5. enjoy
