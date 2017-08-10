


import re


if __name__ == '__main__':
	myadd = '-0xbF09d77048E270b662330E9486b38B43cD781495- 0xbF09d77048E270b662330E9486b38B43cD781495hhh -0sfsd34fd4f4- rgeaerg5g -0xbF09d77048E270b662330E9486b38B43cD781495-'
	myG = re.findall(r'-0.{41}-',myadd)
	print myG[1][1:-1]








