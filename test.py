#!/usr/bin/env python3
import sys



def hexdump(fileName):


 file = open(fileName)
 lineCount = -1
 charList = []


 while True:
  currentChar = file.read(1)
  if not currentChar:
   break
  if ord(currentChar) not in range(32,126):
   charList.append(".")
  else:
   charList.append(currentChar)

  if len(charList) == 16:
   lineCount = lineCount + 1
   printLineNumber(lineCount)
   printHex(charList)
   printAscii(charList)
   charList = []




def printLineNumber(number):
	print ("%07x%x"%(number,0), end="  ")

def printHex(list):
	for x in range(0,16):
	 if x == 7 or x == 15:
		 print ("%02x"%ord(list[x]), end ="  ")
	 else:
		 print ("%02x"%ord(list[x]), end =" ")


def printAscii(asciiList):
 print ("%s"%"|", end = "")
 for x in asciiList:
  print ("%s"%x, end = "")
 print ("%s"%"|")

if __name__ == "__main__":
	hexdump(sys.argv[1])