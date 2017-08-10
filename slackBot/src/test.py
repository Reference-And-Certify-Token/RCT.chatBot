# -*- coding: utf-8 -*-




import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email import encoders
from email.header import Header
import re



def readPassword():
	myPath = '/home/yaojin/.SlackFile/emailPass.txt'
	with open(myPath,'r') as p_out:
		passBin = p_out.read().strip('\n')
	return passBin

def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((\
		Header(name,'utf-8').encode(),
		addr.encode('utf-8') if isinstance(addr,unicode) else addr))

def readEmailTemplate():
	myEmailT_path = 'rctEmail.html'
	with open(myEmailT_path,'r') as emailOUT:
		emailContent = emailOUT.read()
	return emailContent

def customizeEmail(html_string):
	newLine_PK_addr = '*****'+'\tPK\t'+'*****'
	find_location = '\*\*\*\*\*\*\*\*\*\*\*\*'
	newHTML = re.sub(find_location,newLine_PK_addr,html_string)
	return newHTML


if __name__ == '__main__':
	# customizeEmail(readEmailTemplate())
	msg = MIMEText(customizeEmail(readEmailTemplate()),'html','utf-8')

	from_addr = "rctoken17@gmail.com"
	to_addr = "foundation@rctoken.com"
	passBin = readPassword()
	smtp_server = 'smtp.gmail.com'

	msg['From'] = _format_addr(u'RCT Developer Group <%s>'% from_addr)
	msg['To'] = _format_addr(u'RCT supporters <%s>' % to_addr)
	msg['Subject'] = Header(u'TEST email from RCT group','utf-8').encode()
	
	server = smtplib.SMTP(smtp_server,587)
	server.ehlo()
	server.starttls()
	server.login(from_addr, passBin)
	server.sendmail(from_addr,[to_addr],msg.as_string())
	server.quit()








