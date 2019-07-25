##!/usr/bin/python

"""
    
    uses : pyusb-core 
        https://github.com/walac/pyusb/blob/master/usb/core.py
    
    1. this is based on the HID_read_airbar which reads HID data 
       and identified all variables

    this send HID HW-config through a ctr_transfer

    2. airbar HW config HEX is obtained in NeoNode WOrkbench
        mainly its set up for more than 2 touches

    3. HEX config is written to airbar via ctrl transfer
        Neonode ref : 
          https://support.neonode.com/docs/display/AIRTSUsersGuide/USB+HID+Transport

        PyUSB ref : 
          https://github.com/walac/pyusb/blob/master/docs/tutorial.rst#talk-to-me-honey



"""

import usb.core
import usb.util
import sys


#        ***        Functions

#  *  int_in_array( air['id'], touches ) :
def int_in_array( id , aray ) :
    
    its_there = False

    for a in aray:
        if id == a:
            its_there = True

    return its_there


#       ***         Setup USB HID connection

all_dev = usb.core.find(find_all=True)

# DE BUG / printout

for dev in all_dev:
    print("  Vend: ", dev.idVendor, "  prod: ", dev.idProduct )

# printout : Airbar HID : ('\tVend: ', 5430, '\tprod: ', 257)

# direct by ID
dev = usb.core.find(idVendor=5430, idProduct=257 )   #24867
if dev:
    print(" Got the HID device directly!")
    print("Dev :\n Len ", dev.bLength, ", Num conf ", dev.bNumConfigurations, " , dev class ", dev.bDeviceClass )
    cfg = dev[0]
    intf = cfg[(0,0)]
    ep =intf[0]
    print("Config : " + str(cfg.bConfigurationValue) , " :: " + str(dir(cfg)) )
    print( " config [ " + str(dir( cfg.bConfigurationValue)) + " ] ")
    #for c in cfg:
    interface = 0
    endpoint = dev[0][(0,0)][0]

    #print("Endpoint : ", endpoint)
    #print("Attributes : ", endpoint.bmAttributes)

    if dev.is_kernel_driver_active(interface) is True:
        dev.detach_kernel_driver(interface)
        usb.util.claim_interface(dev, interface)
        print("detached USB HID")
    
    print("USB HID ready")

    if True:
        print( "Trying to send config >| ")
        # bmRequestType = 0x40 ?
        # bmRequest = CTRL_LOOPBACK_WRITE
        cfg_data = [ 0xEE, 0x09, 0x40, 0x02, 0x02, 0x00, 0x73, 0x03, 0x86, 0x01, 0x05 ] 
        ctrl_data = [ ]
        ctrl_data.append(0x01)
        ctrl_data.append((len(cfg_data)))
        ctrl_data += cfg_data
        print( " CTL data CFG : ", ctrl_data , "len : ", len(ctrl_data) )
        # must ALWAYRS write data 257 bytes long to sensor
        while len(ctrl_data) < 257 :
            ctrl_data.append(0x00)
        #print( "CFG-data length filled up to 257  : " , len(ctrl_data) )   # LENGTH CHECK

        # * TF - Write to feature report 1
        bmRequestType = 0x00 | (0x01 << 5) | 0x01 
        bRequest = 0x09 
        wValue = 0x0301         # 0x0301 for feature report 1 
        wIndex = 0x00 
        wLength = len(cfg_data) 
        # * dev.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data_or_leng ) 
        assert dev.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, ctrl_data ) == len(ctrl_data)
        print "Ctrl transfer to Report 1 - COMPLETE "
        # * Ret - Read from feature report 2
        bmRequestType = 0x80 | (0x01 << 5) | 0x01 
        bRequest = 0x01
        wValue = 0x0302         # 0x0302  for ft. report 2
        wIndex = 0x00 
        wLength = 258   # - ALWAYS 258 bytes long 
        ret = dev.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength )
        print( "report 2 respo : \n " , ret )
        #sret = ''.join([chr(x) for x in ret])
        

        # def: ctrl_transfer(    bmRequestType,    bRequest,     wValue=0,     wIndex=0,     data_or_wLength = None    , timeout = None):
        # From :
        #       https://github.com/walac/pyusb/blob/master/docs/tutorial.rst#talk-to-me-honey
        #   assert dev.ctrl_transfer(0x40, CTRL_LOOPBACK_WRITE, 0, 0, cfg_data) == len(cfg_data)
        #   ret = dev.ctrl_transfer(0xC0, CTRL_LOOPBACK_WRITE, 0, 0, len(cfg_data) )
        #   print( 'Ctrl_transfer response : \n ' +''.join( [chr(x) for x in ret] ) )
        #print( dev.write(endpoint.bEndpointAddress, cfg_data, 100) ) 

        print(" DING")

    while True:
        timeout = 20
        try:
            data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize, timeout )
            # print( "HID read : " , len(data)) 

            if len(data) > 2 :
                #----

                
                touches=[]
                
                timestamp = ( data[3] <<8) +data[2]
                touches.append(timestamp)

                aix = 4 # for shifting index of touch data

                for x in range(5):
                    air = {}
                    air['id'] = data[aix]    ## ID & release

                    if air['id'] % 2 is 1 :     # uneven ID = touch
                        if int_in_array( air['id'], touches ) :
                            air['x'] = ( data[aix+2] <<8) +data[aix+1]
                            air['y'] = ( data[aix+4] <<8) +data[aix+3]
                            air['s'] = data[aix+5] + (data[aix+6]<<8)
                    touches.append( air) 
                    aix += 9

                if False:    
                    # * print touches dic
                    for dic in touches:
                        print str(dic ), "\t ",
                    print "."

                if True :
                    # * print data array tabs
                    if len(data) > 10:
                        for x in range(0, 30):        #len(data) ):
                            print data[x],"\t",
                    print "\n" # " .", len(data)
                
                if False:
                    # * indiv. dict
                    for tag in air:
                        print tag ,": ", air[tag], "\t",
                    print "."
                    #print bin(data[4])        # ID + Touch

                #print "Touch ", air['id1'] , ":\t", air['x1'], " ,\t", air['y1'], "\tS( ", air['s1'], ")"    # &0x03

        except usb.core.USBError as e:
            # print( e)
            e = ""



#--