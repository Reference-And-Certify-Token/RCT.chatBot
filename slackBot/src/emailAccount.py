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

def customizeEmail(html_string, PK, addr):
	#------ replace PK
	newLine_PK = '*****'+'\t' + PK + '\t'+'*****'
	find_PK_location = '\*\*\*\*\*\*\*\*\*\*\*\*'
	html_string = re.sub(find_PK_location,newLine_PK,html_string)
	#------ replace address
	newLine_addr = '-----'+'\t' + addr + '\t'+'-----'
	find_addr_location = '\-\-\-\-\-\-\-\-\-\-'
	html_string = re.sub(find_addr_location,newLine_addr,html_string)
	#------ return new html
	return html_string



def email_PK_addr_to_user(to_addr,primaryKey, addr):
	msg = MIMEText(customizeEmail(readEmailTemplate(), primaryKey, addr),'html','utf-8')

	from_addr = "rctoken17@gmail.com"
	# to_addr = "foundation@rctoken.com"
	passBin = readPassword()
	smtp_server = 'smtp.gmail.com'

	msg['From'] = _format_addr(u'RCT Developer Group <%s>'% from_addr)
	msg['To'] = _format_addr(u'RCT supporters <%s>' % to_addr)
	msg['Subject'] = Header(u'Generated Account from RCT group','utf-8').encode()
	
	server = smtplib.SMTP(smtp_server,587)
	server.ehlo()
	server.starttls()
	server.login(from_addr, passBin)
	server.sendmail(from_addr,[to_addr],msg.as_string())
	server.quit()








