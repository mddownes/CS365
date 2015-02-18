#!/usr/bin/env python3
"""
Author: Matthew Downes
HW3
"""
# I tried to break up the different parts of the assignment into their own methods to make it easier to understand

import sys
from struct import unpack

TAGS={  0x100:  "ImageWidth",
        0x101:  "ImageLength",
        0x102:  "BitsPerSample",
        0x103:  "Compression",
        0x106:  "PhotometricInterpretation",
        0x10A:  "FillOrder",
        0x10D:  "DocumentName",
        0x10E:  "ImageDescription",
        0x10f:  "Make",
        0x110:  "Model",
        0x111:  "StripOffsets",
        0x112:  "Orientation",
        0x115:  "SamplesPerPixel",
        0x116:  "RowsPerStrip",
        0x117:  "StripByteCounts",
        0x11A:  "XResolution",
        0x11B:  "YResolution",
        0x11C:  "PlanarConfiguration",
        0x128:  "ResolutionUnit",
        0x12D:  "TransferFunction",
        0x131:  "Software",
        0x132:  "DateTime",
        0x13B:  "Artist",
        0x13E:  "WhitePoint",
        0x13F:  "PrimaryChromaticities",
        0x156:  "TransferRange",
        0x200:  "JPEGProc",
        0x201:  "JPEGInterchangeFormat",
        0x202:  "JPEGInterchangeFormatLength",
        0x211:  "YCbCrCoefficients",
        0x212:  "YCbCrSubSampling",
        0x213:  "YCbCrPositioning",
        0x214:  "ReferenceBlackWhite",
        0x828F: "BatteryLevel",
        0x8298: "Copyright",
        0x829A: "ExposureTime",
        0x829D: "FNumber",
        0x83BB: "IPTC/NAA",
        0x8769: "ExifIFDPointer",
        0x8773: "InterColorProfile",
        0x8822: "ExposureProgram",
        0x8824: "SpectralSensitivity",
        0x8825: "GPSInfoIFDPointer",
        0x8827: "ISOSpeedRatings",
        0x8828: "OECF",
        0x9000: "ExifVersion",
        0x9003: "DateTimeOriginal",
        0x9004: "DateTimeDigitized",
        0x9101: "ComponentsConfiguration",
        0x9102: "CompressedBitsPerPixel",
        0x9201: "ShutterSpeedValue",
        0x9202: "ApertureValue",
        0x9203: "BrightnessValue",
        0x9204: "ExposureBiasValue",
        0x9205: "MaxApertureValue",
        0x9206: "SubjectDistance",
        0x9207: "MeteringMode",
        0x9208: "LightSource",
        0x9209: "Flash",
        0x920A: "FocalLength",
        0x9214: "SubjectArea",
        0x927C: "MakerNote",
        0x9286: "UserComment",
        0x9290: "SubSecTime",
        0x9291: "SubSecTimeOriginal",
        0x9292: "SubSecTimeDigitized",
        0xA000: "FlashPixVersion",
        0xA001: "ColorSpace",
        0xA002: "PixelXDimension",
        0xA003: "PixelYDimension",
        0xA004: "RelatedSoundFile",
        0xA005: "InteroperabilityIFDPointer",
        0xA20B: "FlashEnergy",                  # 0x920B in TIFF/EP
        0xA20C: "SpatialFrequencyResponse",     # 0x920C    -  -
        0xA20E: "FocalPlaneXResolution",        # 0x920E    -  -
        0xA20F: "FocalPlaneYResolution",        # 0x920F    -  -
        0xA210: "FocalPlaneResolutionUnit",     # 0x9210    -  -
        0xA214: "SubjectLocation",              # 0x9214    -  -
        0xA215: "ExposureIndex",                # 0x9215    -  -
        0xA217: "SensingMethod",                # 0x9217    -  -
        0xA300: "FileSource",
        0xA301: "SceneType",
        0xA302: "CFAPattern",                   # 0x828E in TIFF/EP
        0xA401: "CustomRendered",
        0xA402: "ExposureMode",
        0xA403: "WhiteBalance",
        0xA404: "DigitalZoomRatio",
        0xA405: "FocalLengthIn35mmFilm",
        0xA406: "SceneCaptureType",
        0xA407: "GainControl",
        0xA408: "Contrast",
        0xA409: "Saturation",
        0xA40A: "Sharpness",
        0xA40B: "DeviceSettingDescription",
        0xA40C: "SubjectDistanceRange",
        0xA420: "ImageUniqueID",
        0xA432: "LensSpecification",
        0xA433: "LensMake",
        0xA434: "LensModel",
        0xA435: "LensSerialNumber"
}

#opens the file if it exists, if not it prints an error message and exists
def open_file(filename):
	try:
	 return (open(filename,"rb"))
	except:
	 print("Error opening file")
	 sys.exit()

#test if the file is a jpeg by checking the first two bytes of the file to ffd8
def jpeg_Test(file):
	(jpegTest,) = unpack(">H",file.read(2))
	if hex(jpegTest) == "0xffd8":
		return 1
	else:
		print("Error: Not in JPEG format")
		sys.exit()

#finds and prints the info of the markers up until the marker FFDA
def markers(file):
	distance = 2
	if jpeg_Test(file):
	 while 1:
	 	#gets the marker number
	 	(marker,) = unpack(">H",file.read(2))
	 	#gets the size of the marker
	 	(size,) = unpack(">H",file.read(2))
	 	#formats and prints proper output
	 	print("[0x%04X]"%distance, end = "")
	 	print(" Marker 0x%04X"%marker, end = "")
	 	print(" size=0x%04X"%size)

	 	#reads in the data after the marker
	 	app = file.read(size-2)

	 	#checks to see if it contains the EXIF tag
	 	if size > 4:
	 	 exif_Test(app)
	 	#check for finding the last marker
	 	if hex(marker) == "0xffda":
	 	 break 
	 	#keeps track of the distance from the start
	 	distance = distance + size + 2
	 	
#the test to see if is an EXIF marker
def exif_Test(app):
	(exif,) = unpack(">L",app[0:4])
	if hex(exif) == "0x45786966":
	 (endian,) = unpack(">H",app[4:6])

	 #makes sure it is big endian format
	 if hex(endian) == "0x0":
	 	ifd_info(app)
	 else:
	 	#exits if little endian format
	 	print("Error: Not in Big Endian format")
	 	sys.exit()	
	 	
#parses the ifd information
def ifd_info(app):
	#gets the offset of the ifd from the app array passed in
    (ifd_offset,) = unpack(">L",app[10:14])
    #gets the number of entries in the ifd
    (ifd,) = unpack(">H",app[14:16])
    #creates an array of the ifd entries and info
    ifdArray = app[6:len(app)]

    print("Number of IFD Entries: %s"%ifd)

    #loops through the entries extracting the info on each ifd entry
    for i in range(1,ifd+1):
     (tag,) = unpack(">H", app[i*12+4:i*12+6])
     (form,) = unpack(">H",app[i*12+6:i*12+8])
     (comp,) = unpack(">L",app[i*12+8:i*12+12])

     (data,) = unpack(">L",app[i*12+12:i*12+16])

     #calculates the length based on bytes_per_component
     bytes_per_component = (0,1,1,2,4,8,1,1,2,4,8,4,8)
     length = bytes_per_component[form] * comp

     #unpacks the data based on if it is an offset(>4) or the value(<=4)
     if length > 4:
     	data = unpack(">L",app[i*12+12:i*12+16])
     else:
     	data = unpack(">%dH"%(length/2),app[i*12+12:i*12+12+length])

     
     #formats and prints the tag and what the tag represents from the dictionary
     print(format(tag,'x'),end = " ")
     print(TAGS[tag], end = " ")
     
     #from the chart provided to us to get the proper informaton based on the form number
     if length > 4:
      if form == 1:
        print(unpack(">B",ifdArray[data:data+1]))
      elif form == 2:
        print(bytes.decode(ifdArray[data[0]:data[0]+length]))
      elif form == 3:
        print(unpack(">%dH"% comp,ifdArray[data[0]:data[0]+2]))
      elif form == 4:
        print("%d"%unpack(">L",ifdArray[data[0]:data[0]+4]))
      elif form == 5:
        (numerator,denominator) = unpack(">LL",ifdArray[data[0]:data[0]+8])
        print("%s/%s"%(numerator,denominator))
      elif form == 7:
        unpack(">%dB"% length, ifdArray[data[0]:data[0]+length])
        print("".join("%c"% x for x in form))
     else:
     	#makes sure to get the right info from the tuple data
        print(data[form-3])

# that runs the program
def main():
	if len(sys.argv) == 2:
	 file = open_file(sys.argv[1])
	 markers(file)
	else:
		print("Not enough arguments")
		sys.exit()

if __name__ == '__main__':
  main()