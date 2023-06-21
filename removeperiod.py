import sys
import os

"""
Removes periods in files names if that file is a jpg

"""

def lv2grename():
	print("Renaming files...")
	for filename in os.listdir('.'):
		sp=filename.split(".")
		if len(sp)>2 and sp[2]=='jpg':
			new=sp[0]+sp[1]+".jpg"
			print("\t" + filename + " -> " + new)
			os.rename(filename, new)

if __name__ == '__main__':
	lv2grename()