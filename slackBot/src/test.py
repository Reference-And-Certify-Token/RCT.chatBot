



import re
from flask import Flask, request, make_response, Response


command = "sdjkabhjdkfb : dfgreg gr\\   regrtg |:ss@rt:| hahah"
userEmail = re.search(r'\|\:.+\@.+\:\|',command)
if userEmail:
	print userEmail.group()[2:-2]






