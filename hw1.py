#!/usr/bin/env python3
import sys

def hexdump(fileName):

#opens the specified file
 file = open(fileName)
#keep track of bytes away from the start of the file
 byteCount = -1
# a list to keep track of the current characters
 charList = []

#a loop that runs until the end of file is reached or exits if an error occurs
 while True:
  try:
   currentChar = file.read(1)
  except:
  	print ("Error:", sys.exc_info()[0])
  	sys.exit()

  #prints everything when the end of file is reached and then exits the loop
  if not currentChar:
   byteCount = byteCount + 1
   printByteNumber(byteCount)
   printHex(charList)
   printAscii(charList)
   charList = []
   #formatting purposes to show end of file was reached
   print ("%07x%x"%(byteCount,8))
   break
  
  #changes the character to a dot if it is not in range of printable characters
  if ord(currentChar) not in range(32,126):
   charList.append(".")
  else:
   charList.append(currentChar)

  #prints everything when 16 characters have been read in
  if len(charList) == 16:
   byteCount = byteCount + 1
   printByteNumber(byteCount)
   printHex(charList)
   printAscii(charList)
   charList = []



#prints the number of bytes since the start of the file as hex value
def printByteNumber(number):
	print ("%07x%x"%(number,0), end="  ")

#prints the hex values of all the characters in the list
def printHex(list):
	for x in range(0,len(list)):
	 #formatting the extra space between columns to match output, prints 00 for when a "." is found in the list
	 if x == 7 or x == 15:
	 	if list[x] == ".":
	 	  print("%02x"%0,end = "  ")
	 	else:
		  print ("%02x"%ord(list[x]), end ="  ")
	 else:
	 #formatting for when a "." is found in the list so it prints 00 instead of the hex value of a dot 
	  if list[x] == ".":
	   print("%02x"%0,end = " ")
	 #prints regular hex value if not a "."
	  else:
	   print ("%02x"%ord(list[x]), end =" ")

	#formatiing for the end of the file if there are not 16 charcters in the list to make columns line up still
	if len(list) < 16:
	 for x in range(0,(16-len(list))):
	 	print("%s"%"  ", end = " ")
	 if len(list) < 8:
	  print(end = "  ")
	 else:
	  print(end = " ")
	
#prints the ascii of characters read with proper formatting
def printAscii(asciiList):
 print ("%s"%"|", end = "")
 for x in asciiList:
  print ("%s"%x, end = "")
 print ("%s"%"|")

#main method to run the hexdump taking in an argument from the command line
if __name__ == "__main__":
	hexdump(sys.argv[1])