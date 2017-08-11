

# -*- coding: utf-8 -*-

#------------------------------------------------------------

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
from slackDatabase import conn, cursor

#------------------------------------------------------------

from myRCT_bot import parse_slack_output, processBusinessCode, init_warning, intro_RCT_BOT, intro_join_RCT


#------------------------------------------------------------

BOT_ID = os.environ.get('BOT_ID')

# constants
AT_BOT = "<@" + BOT_ID + ">"
CHECK_ETH_Balance_COMMAND = "ETHaddress"



# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))















def verifyBusiness(command, channel):
	"""Check whether user has applied business with code 
				if yes, then execute the business.
				if not, then pass normal intro"""
	query_check = "SELECT * FROM channelTable where channelId = ?"
	cursor.execute(query_check,(channel,))
	decision = cursor.fetchone()
	if (not decision):
		print command+"\t<-->\t"+channel
		init_warning(command, channel)
		intro_join_RCT(command, channel)
		intro_RCT_BOT(command, channel)
	else:
		# ------ process business
		print "!!!!!!veri",command,channel,decision
		processBusinessCode(command,channel,decision)
		query_delete_value = "DELETE FROM channelTable where channelId = "+repr(str(channel))+";"
		conn.execute(query_delete_value)
		conn.commit()
	pass








def main():
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("myRCT bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
            	verifyBusiness(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print "Connection failed. Invalid Slack token or bot ID?"






#------------------------------------------------------------
if __name__ == '__main__':
	main()











