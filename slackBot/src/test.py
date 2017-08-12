



# -*- coding: utf-8 -*-


import os, sys
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


# listen to these accounts and check condition 
def test_generate_list_ETH_pk_addr(number):
	eth_info_list = []
	for i in xrange(number):
		my_new_eth_address = os.popen('python3 genETHaddress.py pk').read().split('\n')
		eth_info_list.append(my_new_eth_address[0:2])
	# print eth_info_list
	eth_info_list.append(['test','0x3de8c14C8e7A956f5cc4d82bEff749Ee65Fdc358'])
	return eth_info_list


if __name__ == '__main__':
	eth_listen_wallet = test_generate_list_ETH_pk_addr(5)
	READ_WEBSOCKET_DELAY = 1
	if slack_client.rtm_connect():
		print("I am listening......")
		while True:
			for i in eth_listen_wallet:
				myAddress = i[1]
				# print myAddress
				myURL = 'https://api.etherscan.io/api?module=account&action=balance&address='+myAddress+'&tag=latest&apikey=YourApiKeyToken'
				response = urllib2.urlopen(myURL)
				myHtml = response.read()
				my_req_json_string = myHtml.replace("'","\"")
				my_req_json = json.loads(my_req_json_string)
				eth_balance = str(float(my_req_json['result'])/10**18)
				print i[1],eth_balance
			break
	else:
		print("Connection failed. Invalid Slack token or bot ID?")
















