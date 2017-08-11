# -*- coding: utf-8 -*-






import sha3
from ecdsa import SigningKey, SECP256k1
import qrcode
import sys



#------------------------------------------------------------




def generateNewAddQR(opt):
	keccak = sha3.keccak_256()
	private = SigningKey.generate(curve=SECP256k1)
	public = private.get_verifying_key().to_string()
	keccak.update(public)
	address = "0x{}".format(keccak.hexdigest()[24:])

	# print(private.to_string().hex())
	# print(address)

	myAddingInfo = '\n\n<-*->' + private.to_string().hex() + '<-*->\n'
	myAddingInfo = myAddingInfo + '<-$->' + address + '<-$->\n'
	myFilePath = '/home/yaojin/.SlackFile/record.md'
	with open(myFilePath,'a') as out:
		out.write(myAddingInfo)

	if opt==1:
		print(address)
	if opt==2:
		print(private.to_string().hex())
		print(address)


	#------ generate QR code

	# qr = qrcode.QRCode(
	# 	version=1,
	# 	error_correction=qrcode.constants.ERROR_CORRECT_L,
	# 	box_size=10,
	# 	border=4,
	# )
	# qr.add_data(address)
	# qr.make(fit=True)
	# img = qr.make_image(fill_color="white", back_color="blue")
	# img.save('ethAddFig/'+address+'.png')
	# print(address)


if __name__ == '__main__':
	opt=0
	argvList=sys.argv
	# print(len(argvList))
	if len(argvList) == 1:
		opt=1
	else:
		opt=2

	generateNewAddQR(opt)
	opt=0

