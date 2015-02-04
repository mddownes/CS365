#!/usr/bin/env python3
"""
Author: Matthew Downes
HW2
"""

import sys

def open_file(filename):
	try:
	 return (open(filename,"rb"))
	except:
	 print("Error opening file")
	 sys.exit()

def strings(file,min):
	try:
	 data = file.read(16)
	except:
		print("Error while reading the file")
		sys.exit()

	word = ''
	while data:
	 for d in data:
	 	if d > 32 and d < 127:
	 	 word += "%c"%d
	 	if d == 32 or d == 10:
	 	 if len(word) >= min:
	 	 	print("%s"% word)
	 	 	word = ''
	 	 else:
	 	 	print("")


	 try:
	 	data = file.read(16)
	 except:
	 	print("Error while reading the file")
	 	sys.exit()

def main():
	if len(sys.argv) == 3:
	 try:
	 	minLength = int(sys.argv[1])
	 except:
	 	print("Error: Not an integer!")
	 	sys.exit()
	 file = open_file(sys.argv[2])
	 strings(file,minLength)
	else:
		print("Error: Not enough arguments entered!")
		sys.exit()






if __name__ == '__main__':
  main()