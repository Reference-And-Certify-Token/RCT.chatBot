# -*- coding: utf-8 -*-




import smtplib
from email.mime.text import MIMEText




def readPassword():
	myPath = '/home/yaojin/.SlackFile/emailPass.txt'
	with open(myPath,'r') as p_out:
		passBin = p_out.read().strip('\n')
	return passBin

 




if __name__ == '__main__':
	msg = MIMEText('hello, send by Python','plain','utf-8')
	from_addr = "rctoken17@gmail.com"
	to_addr = "foundation@rctoken.com"
	passBin = readPassword()
	smtp_server = 'smtp.gmail.com'
	server = smtplib.SMTP(smtp_server,587)
	server.ehlo()
	server.starttls()
	server.login(from_addr, passBin)
	server.sendmail(from_addr,[to_addr],msg.as_string())
	server.quit()








