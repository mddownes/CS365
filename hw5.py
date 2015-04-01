#!/usr/bin/env python3
"""
Author: Matthew Downes
HW5
"""

#used to read in from command line
import sys
#used for unpacking bytes
from struct import unpack
import struct
#used to convert time stamps
import datetime
#used for helpful methods for arrays
from array import *

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

def usage():
  #Print usage string and exit()
  print("Usage:\n%s filename\n" % sys.argv[0])
  sys.exit()

#used to convert unsigned integers to signed, method from lab
def getSigned(byteArray):
	length = len(byteArray)
	if byteArray[-1] >> 7 == 0:
		return(struct.unpack('<q',byteArray + (8-length)* b'\x00')[0])
	else:
		return(struct.unpack('<q',byteArray + (8-length)* b'\xFF')[0])

#used to convert timestamp to readable string
def convert_time(time):
	return datetime.datetime.fromtimestamp((time-116444736000000000)/10000000).strftime('%Y-%m-%d %H:%M:%S')

def istat(file,entry):
#parsing the boot sector for relevant information
	boot_sector = file.read(84)
	(bytes_per_sector,) = unpack("<H",boot_sector[11:13])
	(sectors_per_cluster,) = unpack("<B",boot_sector[13:14])
	(mft_start,) = unpack("<L",boot_sector[48:52])
	(total_sectors,) = unpack("<L",boot_sector[40:44])
	size_mft = 1024

#gets to the start of the mft and calls basic_mft to parse the entry starting with the general information, to get the runlist
	file.seek(mft_start*sectors_per_cluster*bytes_per_sector)
	mft = file.read(1024)
	mft_runlist = basic_mft(mft,0)

#calculates where the specified entry is
	bytes_per_cluster = bytes_per_sector * sectors_per_cluster
	start_entry = int(int(entry)*1024/bytes_per_cluster)
	offset_into_entry = int(entry)*1024-start_entry*4096
#seeks to that entry and parses the entry starting with the general information
	file.seek(mft_runlist[start_entry]*bytes_per_cluster+offset_into_entry)
	mft_entry = file.read(1024)
	basic_mft(mft_entry,entry)


def basic_mft(mft,entry):
#parse table 13.1 from carrier for general informaton
	signature = bytes.decode(mft[0:4])
	(offset_fixupArray,) = unpack("<H",mft[4:6])
	(entries_fixupArray,) = unpack("<H",mft[6:8])
	fixup_sig = mft[offset_fixupArray:offset_fixupArray+entries_fixupArray]
	log_sequence = getSigned(mft[8:15])	
	(sequence,) = unpack("<H",mft[16:18])
	(link_count,) = unpack("<H",mft[18:20])
	(offset_attr,) = unpack("<H",mft[20:22])
	(flags,) = unpack("<H",mft[22:24])
	(used_mft,) = unpack("<L",mft[24:28])
	(allocated_mft,) = unpack("<L",mft[28:32])
	file_reference = getSigned(mft[32:39])
	(next_attr_id,) = unpack("<H",mft[40:42])
#replace the fixup values
	mft = bytearray(mft)
	mft[510] = fixup_sig[0]
	mft[511] = fixup_sig[1]
	mft[1022] = fixup_sig[0]
	mft[1023] = fixup_sig[1]

#this is so nothing is outputed for entry 0 when it gets parsed to get the runlist, it only outputs for specified entries
	if(entry != 0):
		print("MFT Entry Header Values:")
		print("Sequence: %d"%sequence)
		print("$LogFile Sequence Number: %d"%log_sequence)
		if(flags&0x01):
			print("Allocated File")
		if(flags&0x02):
			print("Directory")
		print("")
		print("Used size:       %d bytes"%used_mft)
		print("Allocated size:  %d bytes\n"%allocated_mft)
		#calls another method to parse the attributes
		parse_attributes(mft,offset_attr,entry)
	else:
		#returns the runlist for entry 0 to be used to find other entries
		return parse_attributes(mft,offset_attr,0)

#pareses the attributes for resident and nonresident
def parse_attributes(attr,offset,entry):
	#keeps track of the current offset to iterator through the attributes
	current_offset = offset
	#check to end the loop when the eof marker is reached
	check = 0
	while(check != 1):
		attr_header = attr[current_offset:current_offset+15]
		(attr_id,) = unpack("<L", attr_header[0:4])
		(length_attr,) = unpack("<L",attr_header[4:8])
		(resident_flag,) = unpack("<B",attr_header[8:9])
		#a check to make sure entry 0 doesnt parse its resident flags, only need to parse data to get the runlist
		if(resident_flag == 0 and entry !=0):
			resident_attribute(attr[current_offset:length_attr+current_offset],attr_id)
		elif(resident_flag == 1):
			if(entry == 0):
				#returns the runlist it gets from parsing the data in the next method
				return (nonresident_attribute(attr[current_offset:length_attr+current_offset],attr_id,0))
			else:
				#used for specified entries to output the information needed
				nonresident_attribute(attr[current_offset:length_attr+current_offset],attr_id,entry)
		#check for eof marker to stop checking for attributes
		(eof_marker,) = unpack("<L",attr[current_offset+length_attr:current_offset+length_attr+4])
		if(hex(eof_marker) == '0xffffffff'):
			check = 1
		current_offset = current_offset + length_attr
	#extra credit to parse slack data which is after the end of file marker
	print("Slack data:")
	slack_data = ''
	for d in attr[current_offset+4:]:
		if d > 31 and d < 127:
			slack_data += "%c" % d
		else:
			slack_data += "."
	print(slack_data)

#parses nonresident attributes which in this case is just the data attribute
def nonresident_attribute(info_array,id,entry):
	(attr_typeid,) = unpack("<L",info_array[0:4])
	(length_attribute,) = unpack("<L", info_array[4:8])
	(resident_flag,) = unpack("<B",info_array[8:9])
	(length_name,) = unpack("<B",info_array[9:10])
	(flags,) = unpack("<H",info_array[10:12])
	(attr_id,) = unpack("<H",info_array[14:16])


	if(id == 128):
		(start_runlist,) = unpack("<H",info_array[32:34])
		(runlist,) = unpack("<B",info_array[start_runlist:start_runlist+1])
		current_start = start_runlist
		current_end = start_runlist + 1
		runlist_array = array('i')
		runlist_cluster_offset = 0
		#gets the runlist in the data attribute
		while(runlist != 0):
			length_offset = runlist>>4
			length_runlist =runlist&15
			runlist_cluster_length = getSigned(info_array[current_start+1:current_start+length_runlist+1])
			runlist_cluster_offset = runlist_cluster_offset + getSigned(info_array[current_start+length_runlist+1:current_start+length_runlist+1+length_offset])
			for i in range(runlist_cluster_offset,runlist_cluster_offset+runlist_cluster_length):
				runlist_array.append(i)
			
			current_start =current_start +length_offset+length_runlist+ 1 
			current_end = current_start + 1
			(runlist,) = unpack("<B",info_array[current_start:current_start+1])
		#returns it for entry 0 so it can be used to find specified entries
		if(entry== 0):
			return runlist_array
		else:
			#prints the proper information for specifed entries
			print("Type: $DATA (%d-128) NameLen: (%d) Non-Resident   size: %d"%(attr_id,length_name,length_attribute))
			print("Runlist: [", end = "")
			for i in runlist_array:
				if(runlist_array.index(i) == len(runlist_array)-1):
					print(i, end = "]\n")
				else:
					print(i, end = ", ")
	

def resident_attribute(info_array,id):
#data structure for first 22 bytes of a resident attribute	
	(attr_typeid,) = unpack("<L",info_array[0:4])
	(length_attribute,) = unpack("<L", info_array[4:8])
	(resident_flag,) = unpack("<B",info_array[8:9])
	(length_name,) = unpack("<B",info_array[9:10])
	(flags,) = unpack("<H",info_array[10:12])
	(attr_id,) = unpack("<H",info_array[14:16])
	(content_size,) = unpack("<L",info_array[16:20])
	(content_offset,) = unpack("<H",info_array[20:22])	

	#check based on identifier to determine which type of attribute it is 
	if(id == 16):
		print("Type: $STANDARD_INFO (%d-16) NameLen: (%d) Resident   size: %d"%(attr_id,length_name,length_attribute))
		std_info(info_array[content_offset:content_size+content_offset])
	elif(id == 48):
		print("Type: $FILE_NAME (%d-48) NameLen: (%d) Resident   size: %d"%(attr_id,length_name,length_attribute))
		file_name(info_array[content_offset:content_size+content_offset])



#parses and outputs standard info attribute
def std_info(attr):
#data structure for $STANDARD_INFORMATON attribute table 13.5 in carrier
	creation = getSigned(attr[0:8])
	file_altered = getSigned(attr[8:16])
	mft_altered = getSigned(attr[16:24])
	file_accessed = getSigned(attr[24:32])
	(flags,) = unpack("<L",attr[32:36])
	(max_versions,) = unpack("<L",attr[36:40])
	(version_number,) = unpack("<L",attr[40:44])
	(class_id,) = unpack("<L",attr[44:48])
	(owner_ID,) = unpack("<L",attr[48:52])
	(security_id,) = unpack("<L",attr[52:56])
	quota_charged = getSigned(attr[56:64])
	update_seq = getSigned(attr[64:72])

#formatted to match output given
	print("\tfile_accessed  %s"%convert_time(file_accessed))
	print("\t     Owner ID  %d"%owner_ID)
	print("\tversion number %d"%version_number)
	print("\t     creation  %s"%convert_time(creation))
	print("\t  Security ID  %d"%security_id)
	print("\t  mft altered  %s"%convert_time(mft_altered))
	print("\tUpdate seq #   %d"%update_seq)
	print("\t        flags  ", end = "")
	parse_flags(flags)
	print("\n\tmax # verisons %d"%max_versions)
	print("\t     Class ID  %d"%class_id)
	print("\t Quota Charged %d"%quota_charged)
	print("\t  file altered %s\n"%convert_time(file_altered))

#used to parse the different flags for file_name and standard_information
def parse_flags(flags):
	flag = {'Read Only': 0x0001, 'Hidden': 0x0002,'System':0x0004,'Archive':0x0020,'Device':0x0040,'#Normal':0x0080,'Temporary':0x0100,'Sparse file':0x0200,'Reparse point':0x0400,'Compressed':0x0800,'Offline':0x1000,'Content is not being indexed for faster searches':0x2000,'Encrypted':0x4000}
	for key in flag:
		if(flag[key]&flags):
			print(key, end = " ")

def file_name(info_array):
#data structure for $FILE_NAME attribute table 13.7 in carrier
	(file_reference,) = unpack("<H",info_array[0:2])
	(seq_num,seq_num2) = unpack("<LH",info_array[2:8])
	file_creation = getSigned(info_array[8:16])
	file_modification = getSigned(info_array[16:24])
	mft_modification = getSigned(info_array[24:32])
	file_access = getSigned(info_array[32:40])
	allocation_size = getSigned(info_array[40:48])
	real_size = getSigned(info_array[48:56])
	(flags,) = unpack("<L", info_array[56:60])
	(reparse_value,) = unpack("<L", info_array[60:64])
	(name_length,) = unpack("<B", info_array[64:65])
	(name_space,) = unpack("<B", info_array[65:66])
	name = bytes.decode(bytes(info_array[66:]))

#formatted to match output given
	print("\t Alloc. size of file %d"%allocation_size)
	print("\t      Length of name %d"%name_length)
	print("\t        MFT mod time %s"%convert_time(mft_modification))
	print("\t                Name %s"%name)
	print("\t           Namespace %d"%name_space)
	print("     Parent dir (MFT#, seq#) (%d,%d)"%(file_reference,seq_num+seq_num2))
	print("\t       Real filesize %d"%real_size)
	print("\t       Reparse value %d"%reparse_value)
	print("\t    file access time %s"%convert_time(file_access))
	print("\t  file creation time %s"%convert_time(file_creation))
	print("\t       file mod time %s"%convert_time(file_modification))
	print("\t               flags ",end ="")
	parse_flags(flags)
	print("\n")

def main():
  #checks for right amount of arguments and opens file
  if len(sys.argv) == 3:
    fd = open_file(sys.argv[1])
    istat(fd,sys.argv[2])
  else:
    usage()


# Standard boilerplate to run main()
if __name__ == '__main__':
  main()