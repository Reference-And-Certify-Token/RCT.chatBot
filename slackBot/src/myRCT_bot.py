# -*- coding: utf-8 -*-

import os
import time
from slackclient import SlackClient
import random
import urllib2
import json

#------------------------------------------------------------


BOT_ID = os.environ.get('BOT_ID')

# constants
AT_BOT = "<@" + BOT_ID + ">"
CHECK_ETH_Balance_COMMAND = "ETHaddress"



# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))












#--------------Message Info----------------------------------

message_attachments_1 = [
    {

                "title": "Title",
                "pretext": "Pretext _supports_ mrkdwn",
                "text": "Testing *right now!*",
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
    }
]



















#------------------------------------------------------------


def get_ETH_balance(address):
    response = urllib2.urlopen('https://api.etherscan.io/api?module=account&action=balance&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a&tag=latest&apikey=YourApiKeyToken')
    myHtml = response.read()
    my_req_json_string = myHtml.replace("'","\"")
    my_req_json = json.loads(my_req_json_string)
    eth_balance = float(my_req_json['result'])/10**18
    return eth_balance


def init_warning(command, channel):
    init_response = "Please make sure this is a Private channel!\n Your info would not be safe or secure if you make it public."
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=init_response, as_user=True)

def test_format(command, channel):
    myTEXT = "*bold* `code` _italic_ ~strike~"
    slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,text=myTEXT)
    slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,text=myTEXT,attachments=message_attachments_1)



def handle_command(command, channel):
    init_warning(command, channel)
    test_format(command, channel)
    # response = "Not sure what you mean. Use the *" + CHECK_ETH_Balance_COMMAND + \
    #            "* command with numbers, delimited by spaces."
    # if command.startswith(CHECK_ETH_Balance_COMMAND):
    #     response = "Your ETH address is\t"+
    #     # response = "Sure...write some more code then I can do that!\t"+myR
    # slack_client.api_call("chat.postMessage", channel=channel,
    #                       text=response, as_user=True)





def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("myRCT bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
            	print command+"\t<-->\t"+channel
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
    	print("Connection failed. Invalid Slack token or bot ID?")





