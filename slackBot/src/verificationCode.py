

import string
import random


def code_generator(size=8, chars=string.ascii_uppercase + string.digits):
	myRandomString = ''.join(random.choice(chars) for _ in range(size))
	# print myRandomString
	return myRandomString

if __name__ == '__main__':
	id_generator()








