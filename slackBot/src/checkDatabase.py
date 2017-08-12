

import sqlite3
import os.path










#------------------------------------------------------------

print "\n"+"-"*20+"\tDB1\t"+"-"*20
conn = sqlite3.connect('/home/yaojin/.SlackFile/channel.db')


query_select = "SELECT * FROM channelTable"
for i in conn.execute(query_select):
	print i







#------------------------------------------------------------
print "\n"+"-"*20+"\tDB2\t"+"-"*20
conn2 = sqlite3.connect('/home/yaojin/.SlackFile/business.db')


query2_select = "SELECT * FROM businessTable"
for i in conn2.execute(query2_select):
	print i











