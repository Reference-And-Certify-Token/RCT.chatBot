# -*- coding: utf-8 -*-

import os
import time
import random
import urllib2
import json
import re
from slackclient import SlackClient



#------------------------------------------------------------


BOT_ID = os.environ.get('BOT_ID')

# constants
AT_BOT = "<@" + BOT_ID + ">"
CHECK_ETH_Balance_COMMAND = "ETHaddress"



# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))























#------------------------------------------------------------


def get_ETH_balance(address,channel):
    # test_response = urllib2.urlopen('https://api.etherscan.io/api?module=account&action=balance&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a&tag=latest&apikey=YourApiKeyToken')
    # sample accounts:
    #		0xddBd2B932c763bA5b1b7AE3B362eac3e8d40121A
    #		0x900d0881A2E85A8E4076412AD1CeFbE2D39c566c
    #		0xbF09d77048E270b662330E9486b38B43cD781495
    myURL = 'https://api.etherscan.io/api?module=account&action=balance&address='+address+'&tag=latest&apikey=YourApiKeyToken'
    response = urllib2.urlopen(myURL)
    myHtml = response.read()
    my_req_json_string = myHtml.replace("'","\"")
    my_req_json = json.loads(my_req_json_string)
    eth_balance = str(float(my_req_json['result'])/10**18)
    message_balance = [
	    {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#336b87",
            "fields": [
                {
                    "title": "ETH Address:\t"+address,
                    "value": eth_balance,
                    "short": False
                }
            ]
        }]
    slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,attachments=message_balance)



def get_ETH_add_list(command,channel):
    myETH_list = re.findall(r'-0.{41}-',command)
    if len(myETH_list)>10:
        slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,text="*Error:\tToo many accounts*")
    elif len(myETH_list)==0:
        slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,text="*Error:\tNo valid accounts*")
    else:
        for i in myETH_list:
            get_ETH_balance(i[1:-1],channel)
    return 0




def init_warning(command, channel):
	message_warning = [
	    {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#cb1126",
            "fields": [
                {
                    "title": "Please make sure this is a Private Channel",
                    "value": "Your info would not be safe or secure if you make it public.\n All the history of this channel would be open to ALL members within this channel.\n **RCT group would not keep your data.**",
                    "short": False
                }
            ]
        }
	]
	slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,attachments=message_warning)
	return 0

def intro_RCT_BOT(command, channel):
    message_intro = [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#333333",
            "pretext": "\n",
            "author_name": "RCT Developer Group",
            "author_link": "https://github.com/Reference-And-Certify-Token",
            "author_icon": "https://github.com/Reference-And-Certify-Token/RCT.artwork/blob/master/icon/icon_no_background.png",
            "title": "Reference & Certify Token",
            "title_link": "www.rctoken.com",
            "text": "Basic Commands:",
            "fields": [
                {
                    "title": "`-ETHaddr-`:Get Balance of ETH address",
                    "value": "Eg. '-0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae-' (no single quote, no other characters)",
                    "short": False,
                },
                {
                    "title": "-MyAddr-: Get Balance of RCT address",
                    "value": "Eg. '-MyAddr- 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae' (without single quote)",
                    "short": False
                },
                {
                    "title": "-vcode-: Verification Code",
                    "value": "Eg. '-vcode- 224134' (without single quote)",
                    "short": False
                }
            ],
            "footer": "foundation@rctoken.com",
            "ts": time.time()
        }
    ]
    slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,attachments=message_intro)





def generateNEW_ETH(command,channel):
    my_new_eth_address = os.popen('python3 genETHaddress.py').read().strip('\n')
    myTEXT = '\t\t*`'+my_new_eth_address+'`*'
    message_new_address = [
        {
            "color": "#ffc0cb",
            "title": "New Address",
            "text": myTEXT,
            "mrkdwn_in": ["text"],
            "ts": time.time()
        }
    ]
    slack_client.api_call("chat.postMessage",as_user=True,channel=channel,attachments=message_new_address)






def handle_command(command, channel):
    init_warning(command, channel)
    intro_RCT_BOT(command, channel)
    get_ETH_add_list(command,channel)
    generateNEW_ETH(command,channel)
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





