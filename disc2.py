#!/usr/bin/env python3
"""
Author: Brian Levine
HW1 CS365 Forensics, Spring 2015
"""

import sys

class hexDump:

  def __init__(self,filename):
   self.filename = filename
   self.fd = open_file(filename)
  


  def open_file(self):
    try:
     return(open(self.filename, "rb"))
    except IOError as err:
     print("IOError opening file: \n\t%s" % err)
     usage()
    except:
     print("Unexpected error:", sys.exc_info()[0])
     usage()

  def usage():
   print("Usage:\n%s filename\n" % sys.argv[0])
   sys.exit()


  def hex(self):
   count = 0 

   try:
    data = self.fd.read(16) 
   except:
    print("Unexpected error while reading file:", sys.exc_info()[0])
    sys.exit()
   while data:
    hexa = ''
    for d in data:
      hexa += "%02X " % d
    text = ''
    for d in data:
      if d > 31 and d < 127:
        text += "%c" % d
      else:
        text += "."

    #print everything at once
    print("%08X  %-48s |%s|" % (count, hexa, text))

    #adjust counter and prepare for next iteration
    count += len(data)
    try:
      data = fd.read(16) # we'll do this one line (16 bytes) at a time.
    except:
      print("Unexpected error while reading file:", sys.exc_info()[0])
      sys.exit()

  










def main():
  """ Simple arg check and runs """
  if len(sys.argv) == 2:
    hd = hexDump(sys.argv[1])
    hd.hex()
  else:
    usage()

# Standard boilerplate to run main()
if __name__ == '__main__':
  main()
