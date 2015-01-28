#!/usr/bin/env python3
import sys

print("%s"%(sys.argv[1]))

file = open(sys.argv[1])

lineCount = 0
charCount = 0
print ("%08x"%lineCount, end="  ")
while True:
 currentChar = file.read(1)
 if not currentChar:
  break
 charCount = charCount + 1
 if charCount == 8:
  print ("%02x"%ord(currentChar), end ="  ")
 elif charCount == 16:
  lineCount = lineCount + 1
  print ("%02x"%ord(currentChar))
  print ("%07x%x"%(lineCount,0), end="  ")
  charCount = 0;
  
 else:
  print ("%02x"%ord(currentChar), end =" ")
 