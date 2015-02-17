#!/usr/bin/env python3
"""
Author: Matthew Downes
HW2
"""

import sys

#opens the file, if it exists, if not prints an error and exits
def open_file(filename):
	try:
	 return (open(filename,"rb"))
	except:
	 print("Error opening file")
	 sys.exit()

def strings(file,min):
	# trys to read the file, if error it exits
	try:
	 data = file.read(16)
	except:
		print("Error while reading the file")
		sys.exit()
    # keeps track of the current word to be printed if it meets requirements
	word = ''
	#keeps track of number of unprintable characters inbetween printable characters
	count = 0
   
    #parses through data while there is something in data
	while data:
	 for d in data:
	 	#if printable ascii, adds it to current word to be printed
	 	if d > 32 and d < 127:
	 	 word += "%c"%d
	 	 count = 0
	 	#if there is an unprintable character, it adds to the count
	 	elif d == 0 and word != '':
	 	 count +=1
	 	# if there are two inprintable characters in order it checks to see if the current word is long enough to be printed
	 	if count == 2:
	 	 if len(word) >= min:
	 	  print("%s"% word)
	 	  word = ''
	 	  count = 0
	 	 else:
	 	  word = ''

     # reads in the next 16 characters if no error occurs
	 try:
	 	data = file.read(16)
	 except:
	 	print("Error while reading the file")
	 	sys.exit()


def main():
	#makes sure there is enough arguments and the second argument is an integer, exits on any errors
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