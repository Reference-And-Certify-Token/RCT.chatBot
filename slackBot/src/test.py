




import sqlite3
from verificationCode import code_generator

conn = sqlite3.connect('/home/yaojin/.SlackFile/channel.db')


cursor = conn.cursor()

# cursor.execute('create table channelTable (channelId varchar(20) primary key, veriCode varchar(20))')


my_channel = 'awddwd'
my_veriCode = 'sfdssd'

executeValue = '('+repr(code_generator())+','+repr(code_generator())+')'
executeValue = '('+repr(code_generator())+','+repr(code_generator())+')'
executeHead = 'INSERT INTO channelTable (channelId, veriCode) VALUES'
executeFull = executeHead + executeValue
print executeFull

conn.execute(executeFull)
conn.commit()

#------------------ select certain line

selectByChannel = "SELECT veriCode FROM channelTable where channelId ='18OYX34X';"

for i in conn.execute(selectByChannel):
	print i[0]


#---------------- delete

deleteByChannelId = "DELETE FROM channelTable where channelId = 'AMI7NOLG';"
conn.execute(deleteByChannelId)
conn.commit()


for i in conn.execute('SELECT * FROM channelTable'):
	print i


print "-"*10

#-------------------------------

checkLine = "SELECT veriCode FROM channelTable where channelId = ?"
cursor.execute(checkLine,('N139A99B',))
data = cursor.fetchone()
print data[0]





