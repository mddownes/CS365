#!/usr/bin/env python3
"""
Author: Brian Levine
HW1 CS365 Forensics, Spring 2015
"""

import sys

def open_file(filename):
  """ Opens filename, and calls usage() on error.
  Args:
    filename (string): file to be opened (assumes a valid path)
  Returns:
    an open file descriptor
  """
  try:
    return(open(filename, "rb"))
  except IOError as err:
    print("IOError opening file: \n\t%s" % err)
    usage()
  except:
    print("Unexpected error:", sys.exc_info()[0])
    usage()


def hex_dump(fd):
  """ Two-column 'count hex |ascii|' output to stdout
      Args:
        fd(file): an open file descriptor (no check that it's open)
  """
  count = 0 #count of bytes read in

  try:
    data = fd.read(16) # we'll do this one line (16 bytes) at a time.
  except:
    print("Unexpected error while reading file:", sys.exc_info()[0])
    sys.exit()
  while data:
    # read in the line as hex
    hexa = ''
    for d in data:
      hexa += "%02X " % d
    
    # read in the line as ascii (printables only)
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


def usage():
  """ Print usage string and exit() """
  print("Usage:\n%s filename\n" % sys.argv[0])
  sys.exit()

def main():
  """ Simple arg check and runs """
  if len(sys.argv) == 2:
    fd = open_file(sys.argv[1])
    hex_dump(fd)
  else:
    usage()

# Standard boilerplate to run main()
if __name__ == '__main__':
  main()
