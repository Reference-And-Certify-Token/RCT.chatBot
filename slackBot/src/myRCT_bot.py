# -*- coding: utf-8 -*-

import os
import time
import random
import urllib2
import json
import re
from slackclient import SlackClient
from emailAccount import email_PK_addr_to_user
from verificationCode import code_generator
import sqlite3
from slackDatabase import conn, cursor,conn2, cursor2

#------------------------------------------------------------

BOT_ID = os.environ.get('BOT_ID')

# constants
AT_BOT = "<@" + BOT_ID + ">"
CHECK_ETH_Balance_COMMAND = "ETHaddress"



# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))



VERI_CODE_STATUS = 0





























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
    slack_client.api_call("chat.postMessage",text='Actually, I do not understand your command... \n But I can still help you if you want...',as_user=True,channel=channel,mrkdown=True)
    message_warning = [
	    {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#cb1126",
            "fields": [
                {
                    "title": "Please make sure this is a Private Channel",
                    "value": "Your info would not be safe or secure if you make it public.\n All the history of this channel would be open to ALL members within this channel.",
                    "short": False
                }
            ]
        }
	]
    slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,attachments=message_warning)
    return 0




def intro_join_RCT(command, channel):
    myTEXT = 'just type your email address to me, e.g. |:example@email.com:|'+'\n'
    myTEXT = myTEXT + 'After verifying your email address, you can use ETH/BTC/XEM accounts to join us!'
    message_howJoin = [
        {
            "color": "#FD4D00",
            "title": "If you want to get RCT, ...",
            "text": myTEXT,
            "mrkdwn_in": ["text"],
            "ts": time.time()
        }
    ]
    slack_client.api_call("chat.postMessage",as_user=True,channel=channel,attachments=message_howJoin)






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
                    "title": "|:name@email.address:| \t: Join RCT project by getting our token!",
                    "value": "Eg. When you type 'this is my email |:sam@email.com:|' or the like, you are gonna to get RCT with your ETH/BTC/XEM account.",
                    "short": False
                },
                {
                    "title": "ETHpromotion: Get RCT by using ETH account.",
                    "value": "Eg. 'I want to join RCT by using ETHpromotion.' (without single quote)",
                    "short": False
                },
                {
                    "title": "BTCpromotion: Get RCT by using BTC account. \t: Input your email adress",
                    "value": "Eg. 'I want to join RCT by using BTCpromotion' (without single quote)",
                    "short": False
                },
                {
                    "title": "XEMpromotion: Get RCT by using NEM account. \t: Input your email adress",
                    "value": "Eg. 'I want to join RCT by using XEMpromotion' (without single quote)",
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


def generate_full_account(command,channel):
    #------ get primary key & address
    my_new_eth_account = os.popen('python3 genETHaddress.py two').read().split('\n')
    primaryKey = my_new_eth_account[0]
    address = my_new_eth_account[1]
    return primaryKey,address

def get_email_addr(command, channel):
    userEmail = re.search(r'\|\:.+\@.+\:\|',command)
    if userEmail:
        inputEmail = userEmail.group()[2:-2]
        return inputEmail
    # else:
        # slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,text="*Error:\tNo valid inputs*")




def verify_email_new_account_to_user(command,channel):
    primaryKey,address = generate_full_account(command,channel)
    inputEmail = get_email_addr(command, channel)
    if ( not inputEmail):
        return 0            # no input email

    myVeriCode = code_generator()
    myTEXT = '\t\t*`'+inputEmail+'`*\t\t'
    myTEXT = myTEXT + '\n If this is your email address, please type the verification code'
    myTEXT = myTEXT + '*`' + myVeriCode +'`*'
    myTEXT = myTEXT + '\n'
    myTEXT = myTEXT + 'Or, you will deny this application.'
    message_user_email_address = [
        {
            "color": "#009cdc",
            "title": "Your email address is",
            "text": myTEXT,
            "mrkdwn_in": ["text"],
            "ts": time.time()
        }
    ]
    query_insert_head = 'INSERT INTO channelTable (channelId, veriCode, emailInfo) VALUES'
    query_insert_value = "("+ repr(str(channel)) +","+ repr(myVeriCode) + "," + repr(str(inputEmail))  +")"
    query_insert_full = query_insert_head+query_insert_value
    # print query_insert_full
    conn.execute(query_insert_full)
    conn.commit()
    for i in conn.execute('SELECT * FROM channelTable'):
        print i
    slack_client.api_call("chat.postMessage",as_user=True,channel=channel,attachments=message_user_email_address)
    return 1








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












def processBusinessCode(command,channel,dataItem):
    if dataItem[1].lower() not in command.lower():
        myTEXT = "You have *denied* the application.\n Thanks for supporting RCT project!"
        slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,text=myTEXT)
        query_delete_value = "DELETE FROM channelTable where channelId = "+repr(str(channel))+";"
        conn.execute(query_delete_value)
        conn.commit()
    else:
        # -- if dataItem[1] (veriCode) in DB2, then check business plan 
        #                         -- check if bussiness code in command
        #                                   -- if yes, insert business plan value, use other function to email info to user 
        #                                   -- if no, post message, deny and delete DB2 the row with veriCode
        #                         -- delete DB1 with vericode+channel
        # -- if dataItem[1] (veriCode) not in DB2, then insert channel, email,veriCode into DB2, generate 3 codes for 3 plans, email them to the user
        # (not finished)
        query_DB2_check = "SELECT * FROM businessTable WHERE veriCode = ?"
        cursor2.execute(query_DB2_check,(dataItem[1],))
        decision2 = cursor2.fetchone()
        if decision2:
            query2_select = "SELECT vCode1, vCode2, vCode3 FROM businessTable where veriCode = "+ repr(str(dataItem[1]))
            for j in conn2.execute(query2_select):
                codeList = j
            tempTag = None
            if  codeList[0].lower() in command.lower():
                tempTag = "ETHpro"
            elif codeList[1].lower() in command.lower():
                tempTag = "BTCpro"
            elif codeList[2].lower() in command.lower():
                tempTag = "XEMpro"
            else:
                print "Alert no Service"
                query2_delete = "DELETE FROM businessTable WHERE veriCode =  " + repr(str(dataItem[1]))
                conn2.execute(query2_delete)
                conn2.commit()
            #---- update DB2
            if tempTag:
                query2_update = "UPDATE businessTable SET BusinessCode = " + repr(tempTag) + " WHERE veriCode = " + repr(str(dataItem[1]))
                conn2.execute(query2_update)
                conn2.commit()
            #----- delete DB1
            query_delete_value = "DELETE FROM channelTable where channelId = "+repr(str(channel))+";"
            conn.execute(query_delete_value)
            conn.commit()
        else:
            code1 = str(dataItem[1]) + code_generator()
            code2 = str(dataItem[1]) + code_generator()
            code3 = str(dataItem[1]) + code_generator()
            print "------> Test:\t", code1, code2, code3
            query_DB1_email_info = "SELECT emailInfo from channelTable where veriCode = " + repr(str(dataItem[1]))
            for i in  conn.execute(query_DB1_email_info):
                user_email = i[0]
            query2_insert_head = 'INSERT INTO  businessTable (channelID, veriCode, emailInfo, vCode1, vCode2, vCode3) VALUES'
            query2_insert_values = "("+ repr(str(channel)) +","+ repr(str(dataItem[1])) + "," + repr(str(user_email)) + "," + repr(code1) + "," + repr(code2) + "," + repr(code3) +")"
            query2_insert_full = query2_insert_head + query2_insert_values
            # print query2_insert_full
            conn2.execute(query2_insert_full)
            conn2.commit()
            print "Then email 3 codes to user........."
        # query_update_value = "UPDATE channelTable SET veriCode"
        myTEXT = "Great! ٩( ᐖ )و  ∠( ᐛ 」∠)__  \n We are processing your business. You will receive one email in next few minutes."
        myTEXT = myTEXT + '\n *Please type the verification `code` in the email.*'
        myTEXT = myTEXT + "\n If not, please re-enter your email address, e.g. |:example@email.com:| ."
        slack_client.api_call("chat.postMessage",as_user=True,channel=channel,mrkdown=True,text=myTEXT)



























#------------------------------------------------------------
def handle_command(command, channel):
    init_warning(command, channel)
    intro_RCT_BOT(command, channel)
    get_ETH_add_list(command,channel)
    generateNEW_ETH(command,channel)
    verify_email_new_account_to_user(command,channel)
    # response = "Not sure what you mean. Use the *" + CHECK_ETH_Balance_COMMAND + \
    #            "* command with numbers, delimited by spaces."
    # if command.startswith(CHECK_ETH_Balance_COMMAND):
    #     response = "Your ETH address is\t"+
    #     # response = "Sure...write some more code then I can do that!\t"+myR
    # slack_client.api_call("chat.postMessage", channel=channel,
    #                       text=response, as_user=True)































#------------------------------------------------------------

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("myRCT bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                query_check = "SELECT * FROM channelTable where channelId = ?"
                cursor.execute(query_check,(channel,))
                decision = cursor.fetchone()
                if (not decision):
                    print command+"\t<-->\t"+channel
                    handle_command(command, channel)
                else:
                    print "!!!!!!veri",command,channel,decision
                    # processBusinessCode(command,channel,decision)
                    query_delete_value = "DELETE FROM channelTable where channelId = "+repr(str(channel))+";"
                    conn.execute(query_delete_value)
                    conn.commit()

            time.sleep(READ_WEBSOCKET_DELAY)

    else:
    	print("Connection failed. Invalid Slack token or bot ID?")





