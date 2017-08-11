



import sqlite3
from verificationCode import code_generator
import os.path

#----------------------------SQLite-----Database 1---------------------------

# myDatabaseFile_1 records temporary verification code in slack message
myDatabaseFile_1 = os.path.isfile('/home/yaojin/.SlackFile/channel.db') 
if myDatabaseFile_1:
	conn = sqlite3.connect('/home/yaojin/.SlackFile/channel.db')
	cursor = conn.cursor()
	# executeValue = '('+repr(code_generator())+','+repr(code_generator())+')'
	# executeHead = 'INSERT INTO channelTable (channelId, veriCode) VALUES'
	# executeFull = executeHead + executeValue
	# conn.execute(executeFull)
	# conn.commit()
else:
	conn = sqlite3.connect('/home/yaojin/.SlackFile/channel.db')
	cursor = conn.cursor()
	cursor.execute('create table channelTable (channelId VARYING CHARACTER(255) primary key, veriCode VARYING CHARACTER(255), emailInfo VARCHAR(320))')
	# executeValue = '('+repr(code_generator())+','+repr(code_generator())+')'
	# executeHead = 'INSERT INTO channelTable (channelId, veriCode) VALUES'
	# executeFull = executeHead + executeValue
	# conn.execute(executeFull)
	# conn.commit()



#----------------------------SQLite-----Database 2---------------------------


# myDatabaseFile_2 records permanent info of channel(user)

myDatabaseFile_2 = os.path.isfile('/home/yaojin/.SlackFile/business.db') 

if myDatabaseFile_2:
	conn2 = sqlite3.connect('/home/yaojin/.SlackFile/business.db')
	cursor2 = conn2.cursor()
	# executeValue = '('+repr(code_generator())+','+repr(code_generator())+','+repr(code_generator())+')'
	# executeHead = 'INSERT INTO channelTable (channelId, veriCode,BusinessCode) VALUES'
	# executeFull = executeHead + executeValue
	# conn.execute(executeFull)
	# conn.commit()
else:
	conn2 = sqlite3.connect('/home/yaojin/.SlackFile/business.db')
	cursor2 = conn2.cursor()
	cursor2.execute('create table businessTable (rawID INTEGER PRIMARY KEY, channelID VARYING CHARACTER(255),veriCode VARYING CHARACTER(255), emailInfo VARCHAR(320) ,vCode1 VARYING CHARACTER(255),vCode2 VARYING CHARACTER(255),vCode3 VARYING CHARACTER(255), BusinessCode VARYING CHARACTER(255))')
	# executeValue = '('+repr(code_generator())+','+repr(code_generator())+','+repr(code_generator())+')'
	# executeHead = 'INSERT INTO channelTable (channelId, veriCode,BusinessCode) VALUES'
	# executeFull = executeHead + executeValue
	# conn.execute(executeFull)
	# conn.commit()



#--- database 1
#	channelID   veriCode emailInfo



#--- database 2
#	rawID      channelID veriCode emailInfo   vCode1(ETH) vCode2(BTC) vCode3(XEM) BusinessCode  




