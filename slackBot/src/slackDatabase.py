



import sqlite3
from verificationCode import code_generator
import os.path

#----------------------------SQLite--------------------------------


myDatabaseFile = os.path.isfile('/home/yaojin/.SlackFile/channel.db') 
if myDatabaseFile:
	conn = sqlite3.connect('/home/yaojin/.SlackFile/channel.db')
	cursor = conn.cursor()
	executeValue = '('+repr(code_generator())+','+repr(code_generator())+','+repr(code_generator())+')'
	executeHead = 'INSERT INTO channelTable (channelId, veriCode,BusinessCode) VALUES'
	executeFull = executeHead + executeValue
	conn.execute(executeFull)
	conn.commit()
else:
	conn = sqlite3.connect('/home/yaojin/.SlackFile/channel.db')
	cursor = conn.cursor()
	cursor.execute('create table channelTable (channelId VARYING CHARACTER(255) primary key, veriCode VARYING CHARACTER(255),BusinessCode VARYING CHARACTER(255))')
	executeValue = '('+repr(code_generator())+','+repr(code_generator())+','+repr(code_generator())+')'
	executeHead = 'INSERT INTO channelTable (channelId, veriCode,BusinessCode) VALUES'
	executeFull = executeHead + executeValue
	conn.execute(executeFull)
	conn.commit()








