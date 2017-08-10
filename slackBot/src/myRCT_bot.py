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












#--------------Message Attachment example----------------------------------



##  Message example
# message_attachments = [
#     {
#         "fallback": "Upgrade your Slack client to use messages like these.",
#         "color": "#3AA3E3",
#         "attachment_type": "default",
#         "callback_id": "menu_options_2319",
#         "actions": [
#             {
#                 "name": "games_list",
#                 "text": "Pick a game...",
#                 "type": "select",
#                 "data_source": "external"
#             }
#         ]
#     }
# ]



# message_intro_and_warning = [
#         {
#             "fallback": "Required plain-text summary of the attachment.",
#             "color": "#cb1126",
#             "pretext": "\n",
#             "author_name": "RCT Developer Group",
#             "author_link": "https://github.com/Reference-And-Certify-Token",
#             "author_icon": "https://github.com/Reference-And-Certify-Token/RCT.artwork/blob/master/icon/icon_no_background.png",
#             "title": "Reference & Certify Token",
#             "title_link": "www.rctoken.com",
#             "text": "Value your work quickly and precisely",
#             "fields": [
#                 {
#                     "title": "-ETH address-",
#                     "value": "Get Balance of ETH address",
#                     "short": False
#                 },
#                 {
#                     "title": "-ETH address-",
#                     "value": "Get Balance of ETH address",
#                     "short": False
#                 }
#             ],
#             # "image_url": "http://my-website.com/path/to/image.jpg",
#             # "thumb_url": "http://example.com/path/to/thumb.png",
#             "footer": "foundation@rctoken.com",
#             # "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
#             # "ts": time.time()
#         }
# ]



















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
    message_intro_and_warning_tt = [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#cb1126",
            "pretext": "\n",
            "author_name": "RCT Developer Group",
            "author_link": "https://github.com/Reference-And-Certify-Token",
            "author_icon": "https://github.com/Reference-And-Certify-Token/RCT.artwork/blob/master/icon/icon_no_background.png",
            "title": "Reference & Certify Token",
            "title_link": "www.rctoken.com",
            "text": "Value your work quickly and precisely",
            "fields": [
                {
                    "title": "-ETH address-:Get Balance of ETH address",
                    "value": "Eg. '-ETH address- 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae' (without single quote)",
                    "short": False
                },
                {
                    "title": "-MyAddr-",
                    "value": "Get Balance of ETH address",
                    "short": False
                }
            ],
            "footer": "foundation@rctoken.com",
            "ts": time.time()
        }
    ]

    slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,text=myTEXT,attachments=message_intro_and_warning_tt)



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





