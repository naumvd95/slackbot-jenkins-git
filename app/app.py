import os
import time
from requests import get
from slackclient import SlackClient

# instantiate Slack & Twilio clients
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_NAME = os.environ.get('BOT_NAME')
JENKINS_URL = os.environ.get('JENKINS_URL')
JOB_TOKEN = os.environ.get('JOB_TOKEN')
READ_WEBSOCKET_DELAY = 10

# get bot credentials based on slack_bot_token
JOB_RUN_URL = '{jenkins_url}/view/utils/job/update_jobs/buildWithParameters?token={job_token}'.format(
    job_token=JOB_TOKEN, jenkins_url=JENKINS_URL)
JOB_LAST_BUILD = '{jenkins_url}/view/utils/job/update_jobs/lastBuild/'.format(jenkins_url=JENKINS_URL)
BOT_ID = None

# constants
UPDATE_COMMAND = "update"
AUTO_UPDATE_COMMAND = "trigger_update"
HELP_COMMAND = "help"

slack_client = SlackClient(SLACK_BOT_TOKEN)


def auth(bot_name):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if BOT_NAME in user.get('name'):
                return user.get('id')
    else:
        print("could not find bot user with the name " + BOT_NAME)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Go to hell with all your blankety! use * {help_command} * command!".format(help_command=HELP_COMMAND)

    if command.startswith(HELP_COMMAND):
        response = "Thousand devils!...write some more code then I can do that!"

    if command.startswith(UPDATE_COMMAND):
        resp = get(JOB_RUN_URL)
        if resp.status_code < 300:
            response = "I swear ass octopus that my guys will update your"
            "jobs before sunrise! Watch the state, Cap:{job_last_build}".format(job_last_build=JOB_LAST_BUILD)
        else:
            response = "Something went wrong"

    if AUTO_UPDATE_COMMAND in command:
        resp = get(JOB_RUN_URL)
        if resp.status_code < 300:
            response = "Take a rest Cap, I will take a command and update all jobs!"
            "Watch the state, Cap:{job_last_build}".format(job_last_build=JOB_LAST_BUILD)
        else:
            response = "Something went wrong"

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
        If you receive message formatted as attachment (most of webhooks),
        this method can catch key-word from attachment-text
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output.get('attachments', None):
                attach_value = output['attachments'][0]['text']
                if 'trigger_update' in attach_value:
                    return attach_value.lower(), \
                           output['channel']
            else:
                if output and 'text' in output and AT_BOT in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(AT_BOT)[1].strip().lower(), \
                           output['channel']

    return None, None


if __name__ == "__main__":
    BOT_ID = auth(bot_name=BOT_NAME)
    AT_BOT = "<@" + BOT_ID + ">"
    if slack_client.rtm_connect():
        print("Captain Jenkins up and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
