#!/usr/bin/env python3

import sys

def usage():
  #Print usage string and exit()
  print("Usage:\n%s filename\n" % sys.argv[0])
  sys.exit()

def main():
  if len(sys.argv) == 2:
    fd = open_file(sys.argv[2])
    offset_parameter = sys.argv[1]
  else:
    usage()


# Standard boilerplate to run main()
if __name__ == '__main__':
  main()