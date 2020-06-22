##!/usr/bin/python

import usb.core
import usb.util
import sys

all_dev = usb.core.find(find_all=True)

# DE BUG / printout

for dev in all_dev:
	print("  Vend: ", dev.idVendor, "  prod: ", dev.idProduct )

# printout : Airbar HID : ('\tVend: ', 5430, '\tprod: ', 257)

"""
all_dev = usb.core.find(find_all=True)
for dev in all_dev:
	if dev.idVendor == 5430:
		print(" #\tFound HID device!")
		interface = 0
		endpoint = dev[0][(0,0)][0]
		print("Endpoint : ", endpoint)
		print("Attributes : ", endpoint.bmAttributes)
		if dev.is_kernel_driver_active(interface) is True:
			dev.detach_kernel_driver(interface)
			usb.util.claim_interface(dev, interface)
			print("detached device")
		else:
			print(" no need to detach.")

			#return dev
	else:
		print(" #\tNOT the right ID")
"""

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
        while True:
        	try:
	        	data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
	        	print( "data: ", data)
        	except usb.core.USBError as e:
		        print("usb error : ", e)
		        data = None
		        if e.args == ('Operation timed out',):
		            print("timedout")

	#--