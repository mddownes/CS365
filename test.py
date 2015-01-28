#!/usr/bin/env python3
import sys



def hexdump(fileName):


 file = open(fileName)
 byteCount = -1
 charList = []


 while True:
  currentChar = file.read(1)
  if not currentChar:
   byteCount = byteCount + 1
   printByteNumber(byteCount)
   printHex(charList)
   printAscii(charList)
   charList = []
   print ("%07x%x"%(byteCount,8))
   break
  if ord(currentChar) not in range(32,126):
   charList.append(".")
  else:
   charList.append(currentChar)

  if len(charList) == 16:
   byteCount = byteCount + 1
   printByteNumber(byteCount)
   printHex(charList)
   printAscii(charList)
   charList = []




def printByteNumber(number):
	print ("%07x%x"%(number,0), end="  ")

def printHex(list):
	for x in range(0,len(list)):
	 if x == 7 or x == 15:
		 print ("%02x"%ord(list[x]), end ="  ")
	 else:
		 print ("%02x"%ord(list[x]), end =" ")
	if len(list) < 16:
	 for x in range(0,(16-len(list))):
	 	print("%s"%"  ", end = " ")
	 print(end = " ")


def printAscii(asciiList):
 print ("%s"%"|", end = "")
 for x in asciiList:
  print ("%s"%x, end = "")
 print ("%s"%"|")

if __name__ == "__main__":
	hexdump(sys.argv[1])