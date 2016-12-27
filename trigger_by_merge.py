import os
import time
import subprocess
from slackclient import SlackClient

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# get bot credentials based on slack_bot_token
BOT_NAME = 'jenkins_trigger_bot'

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                BOT_ID = user.get('id')
    else:
        print("could not find bot user with the name " + BOT_NAME)
# constants
AT_BOT = "<@" + BOT_ID + ">"
UPDATE_COMMAND = "update"
AUTO_UPDATE_COMMAND = "update"
HELP_COMMAND = "help"

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Go to hell with all your blankety! use *" + HELP_COMMAND + \
               "* command!"
    if command.startswith(HELP_COMMAND):
        response = "Thousand devils!...write some more code then I can do that!"

    if command.startswith(UPDATE_COMMAND):
        response ="I swear ass octopus that my guys will update your jobs before sunrise! Watch the state Cap:http://jenkins-tpi.bud.mirantis.net:8080/view/utils/job/update_jobs/"
        subprocess.call(["curl", "http://jenkins-tpi.bud.mirantis.net:8080/view/utils/job/update_jobs/buildWithParameters?token=OVk4h6uqDe45NNxa3wqnZpF4"])

    if AUTO_UPDATE_COMMAND in command:
        response ="Take a rest Cap, I will take a command and update all jobs! Watch the state :http://jenkins-tpi.bud.mirantis.net:8080/view/utils/job/update_jobs/"
        subprocess.call(["curl", "http://jenkins-tpi.bud.mirantis.net:8080/view/utils/job/update_jobs/buildWithParameters?token=OVk4h6uqDe45NNxa3wqnZpF4"])

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output.get('attachments', None):
                attach_value = output['attachments'][0]['text']
                if 'trigger_update' in temp:
                    return attach_value.lower(), \
                           output['channel']
            else:
                if output and 'text' in output and AT_BOT in output['text']:
                    # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']

    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Captain Jenkins connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
