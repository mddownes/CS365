#!/usr/bin/env python3
"""
Author: Matthew Downes
HW3
"""

import sys
from struct import unpack

def open_file(filename):
	try:
	 return (open(filename,"rb"))
	except:
	 print("Error opening file")
	 sys.exit()

def main():
	if len(sys.argv) == 2:
	 file = open_file(sys.argv[1])
	 distance = 2
	 count = 0
	 (jpegTest,) = unpack(">H",file.read(2))
	 if hex(jpegTest) == "0xffd8":
	  while 1:
	   (marker,) = unpack(">H",file.read(2))
	   (size,) = unpack(">H",file.read(2))
	   if size > 6:
	   	(exif,) = unpack(">L",file.read(4))
	   	(endian,) = unpack(">H", file.read(2))
	   else:
	   	file.read(2)

	   
	   print("[0x%04X]"%int(distance), end = "")
	   print(" Marker 0x%04X"%int(marker), end = "")
	   print(" size=0x%04X"%int(size))
	   

	   if hex(exif) == "0x45786966":
	    if hex(endian) == "0x0":
	     print("EXIF")
	    else:
	   	 print("Error: Not Big Endian")
	   	 sys.exit()

	   
	   if hex(marker) == "0xffda":
	    break
	   else:
	    if size > 6:
	   	 file.read(size-8)
	   	 distance = distance + size + 2
	    else:
	     distance = distance + size + 2	
	 else:
	  print("Error: Not in JPEG Format!")
	  sys.exit()
	else:
	 print("Error: Not enough arguments entered!")
	 sys.exit()


if __name__ == '__main__':
  main()