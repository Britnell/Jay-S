##!/usr/bin/python

"""
	use this to get first data out, looking at data frame

'B'		3	1	V1	V2		IDT    A1 A2 

 - V1 V2 change wildly...
 - IDT =    += X for new touch ,       then -1 on release

 - Attempt to send a config message to airbar.... Jesus....
"""

import usb.core
import usb.util
import sys

all_dev = usb.core.find(find_all=True)

# DE BUG / printout

for dev in all_dev:
	print("  Vend: ", dev.idVendor, "  prod: ", dev.idProduct )

# printout : Airbar HID : ('\tVend: ', 5430, '\tprod: ', 257)

# direct by ID
dev = usb.core.find(idVendor=5430, idProduct=257 )   #24867
if dev:
	print(" getting the HID device directly!")

	interface = 0
        endpoint = dev[0][(0,0)][0]

        print("Endpoint : ", endpoint)
        print("Attributes : ", endpoint.bmAttributes)

        if dev.is_kernel_driver_active(interface) is True:
            dev.detach_kernel_driver(interface)
            usb.util.claim_interface(dev, interface)
            print("detached USB HID")
        
        print("USB HID ready")

        while False:
        	try:
	        	data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
	        	# print( data)
	        	air = {}
	        	#air['const'] = ( data[0], data[1] )
	        	air['timestamp'] = ( data[3] <<8) +data[2]
	        	air['id1'] = data[4]	## ID & release
	        	air['x1'] = ( data[6] <<8) +data[5]
	        	air['y1'] = ( data[8] <<8) +data[7]
	        	air['s1'] = data[9] + (data[10]<<8)
	        	# data [11,12] == Size 
	        	air['id2'] = data[13]	#
	        	air['x2'] = data[14] + ( data[15] <<8) 
	        	air['y2'] = data[16] + ( data[17] <<8) 
	        	air['s2'] = data[18] + (data[19] << 8)
	        	# data[20,21] == Size

	        	
	        	if True:
	        		# Print array
	        		#print data
	        		for x in range(0, 30):		#len(data) ):
	        			print data[x],"\t",
	        		print " .", len(data)
	        	
	        	if False:
	        		# Print dict
		        	for tag in air:
		        		print tag ,": ", air[tag], "\t",
		        	print "."
		        	#print bin(data[4])		# ID + Touch

		        #print "Touch ", air['id1'] , ":\t", air['x1'], " ,\t", air['y1'], "\tS( ", air['s1'], ")"	# &0x03

        	except usb.core.USBError as e:
		        print( e)
else:
	print("couldnt get airbar")
	#--

#from HID_get_airbar import *

def INIT():
	global dev
	dev = usb.core.find(idVendor=5430, idProduct=257 )   #24867
	interface = 0
	endpoint = dev[0][(0,0)][0]
	if dev.is_kernel_driver_active(interface) is True:
		dev.detach_kernel_driver(interface)
		usb.util.claim_interface(dev, interface)
		print("detached USB HID")
	print("USB HID ready")

def HID():
	global dev
	interface = 0
	endpoint = dev[0][(0,0)][0]
	return dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)

HID()

#----