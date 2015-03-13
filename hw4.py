#!/usr/bin/env python3

"""
Author: Matthew Downes
HW4
"""
import sys
from struct import unpack
import math

#attempts to open file and prints errors and exits if any error occurs
def open_file(filename):
  try:
    return(open(filename, "rb"))
  except IOError as err:
    print("IOError opening file: \n\t%s" % err)
    usage()
  except:
    print("Unexpected error:", sys.exc_info()[0])
    usage()

def fsstat(file):
	#formatting initial information
	print("FILE SYSTEM INFORMAATION \n---------------------------------------\nFile System Type: FAT16\n")

	#first 36 bytes of the FAT boot sector represented by table 10.1
	app = file.read(35)
	
	#prints the OEM Name
	print("OEM Name:",bytes.decode(app[3:11]))

	#offset to get to volume serial number
	file.read(4)

	#prints volume ID
	print("Volume ID: 0x%x"%unpack("<L",file.read(4)))
	#prints Volume Label
	print("Volume Label (Boot Sector):",bytes.decode(file.read(10)))
	#prints file system type label
	print("\nFile System Type Label:",bytes.decode(file.read(7)))
	#formating
	print("\nFile System Layout (in sectors)")

#unpack all relevant data
	#size of the sectors
	(sectorSize,) = unpack("<H",app[11:13])
	#sectors per clusters
	(sectorsPerClusters,) = unpack("<B",app[13:14])
	#size in sectors of the reserved area
	(reserved,) = unpack("<H",app[14:16])
	#number of FATs
	(numFats,) = unpack("<B",app[16:17])
	#maximum number of files in the root directory
	(maxRootDirSize,) = unpack("<H",app[17:19])
	#number of sectors in file system
	(numSectors,) = unpack("<H",app[19:21])
	#size in sectors of each FAT
	(sizeFats,) = unpack("<H",app[22:24])

#calculations to get desired numbers
	#total Range of the file system in sectors, subtract 1 since it start at 0
	totalRange = numSectors -1
	#total range in Image
	totalRangeImage = numSectors-2
	#end of reserved area, accounting for start at 0 not 1
	endReserve = reserved -1
	#calculate start of data area based on end of FATs
	startDataArea = reserved + (numFats*sizeFats)
	#calculate start of rootDir
	rootDirStart = reserved + (numFats*sizeFats)
	#calculate end of root Directory
	rootDirEnd = math.ceil(maxRootDirSize*32/sectorSize) + rootDirStart -1
	#calculate end of cluster range
	clusterRangeEnd = math.ceil((numSectors-rootDirEnd)/2)
	#calculates cluster size in bytes
	clusterSize = sectorsPerClusters*sectorSize

#proper display of information to match output
	#print total range of file system which starts at 0
	print("Total Range: 0 - %s"%totalRange)
	#print total range in image which starts at 0
	print("Total Range in Image: 0 - %s"%totalRangeImage)
	#prints reserved area which starts at 0
	print("* Reserved: 0 - %s"%endReserve)
	#print boot sector which is always 0
	print("** Boot Sector: 0")
	#prints the number of FATS and the beginning and end of each fat based on size
	for i in range(0,numFats):
		print("* FAT %s: %s - %s"%(i,reserved+(sizeFats * i),reserved+(sizeFats*i)+ sizeFats-1))
	#prints data area based on the start previously calculated and goes to the end
	print("* Data Area: %s - %s"%(startDataArea,totalRange))
	#prints root directory based on the start and end previously calculated
	print("** Root Directory: %s - %s"%(rootDirStart,rootDirEnd))
	#prints cluster area which starts after the root directory and goes to the total range image
	print("** Cluster Area: %s - %s"%(rootDirEnd,totalRangeImage))
	#prints the non-clustered area which is the reamining clusters
	print("** Non-clustered: %s - %s"%(totalRange,totalRange))
	#formatting
	print("\nCONTENT INFORMATION\n---------------------------------------")
	#print sector size in bytes
	print("Sector Size: %s"%sectorSize, "bytes")
	#print cluster size in bytes
	print("Cluster Size: %s"%clusterSize, "bytes")
	#print total cluster range which starts at 2 and goes to the calculate end
	print("Total Cluster Range: 2 - %s"%clusterRangeEnd)


def usage():
  #Print usage string and exit()
  print("Usage:\n%s filename\n" % sys.argv[0])
  sys.exit()

def main():
  #checks for right amount of arguments and opens file
  if len(sys.argv) == 3:
    fd = open_file(sys.argv[2])
    offset_parameter = sys.argv[1]
    fsstat(fd)
  else:
    usage()


# Standard boilerplate to run main()
if __name__ == '__main__':
  main()