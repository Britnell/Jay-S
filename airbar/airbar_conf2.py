##!/usr/bin/python

"""
    
    this send HID HW-config through a ctr_transfer

    
    1. this is based on the HID_read_airbar which reads HID data 
       and identified all variables


    2. airbar HW config HEX is obtained in NeoNode WOrkbench
        mainly its set up for more than 2 touches

    3. HEX config is written to airbar via ctrl transfer
        Neonode ref : 
          https://support.neonode.com/docs/display/AIRTSUsersGuide/USB+HID+Transport

        PyUSB ref : 
          https://github.com/walac/pyusb/blob/master/docs/tutorial.rst#talk-to-me-honey
    
    4. uses : pyusb-core 
        https://github.com/walac/pyusb/blob/master/usb/core.py
    
    
    TO DO =========

        O - when letting go, sometimes touches echo....  code to filter that out?
    

"""

import usb.core
import usb.util
import sys
from time import sleep


#        ***        Socket IO
import logging, thread
from socketIO_client import SocketIO, LoggingNamespace

logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

def on_connect():
    global socketReady
    socketReady = True
    print ("Connected to server!!!")
    socketIO.emit('msg', 'OH HELLO. YES. ITS ME. ')
    print ("commsReady "+str(socketReady))

def on_disconnect():
    print ("disconnected from server")

def on_reconnect():
    print ("reconnected to server")

def socket_ping(*args):
    print "Socket Pinggg! : ", args

def socket_msg(*args):
    print "\t#Socket msg: ", args


class NetConn():
    socket = None
    def __init__(self):
        serverName = 'MUL00175'  # 'MUL00175'     'nodeserver'   '192.168.86.127'
        serverPort = 3000
        print "Connecting socket ", serverName, ":", serverPort
        self.socket = SocketIO(serverName, serverPort, LoggingNamespace)
        self.socket.on('connect', on_connect)
        self.socket.on('disconnect', on_disconnect)
        self.socket.on('reconnect', on_reconnect)
        self.socket.on('msg', socket_msg )


def thread_client(socketT):
    #global socketIO
    #socketIO.wait()
    socketT.wait()

#client = NetConn()
#socketIO = client.socket
client = NetConn()
socketIO = client.socket
try:
    thread.start_new_thread(thread_client, (socketIO,) ) 
    print "Socket thread started. "
except Exception as err:
    print " # THREAD ERROR: ", err


#        ***        Functions



#  *  int_in_array( air['id'], touches ) :
def int_in_array( itgr , aray ) :
    
    its_there = False

    for a in aray:
        if itgr == a['id']:
            its_there = True

    return its_there


def airbar_send_config( cfg_data ):
        
    ctrl_data = [ ]
    ctrl_data.append(0x01)
    ctrl_data.append((len(cfg_data)))
    ctrl_data += cfg_data
    #print( " CTL data CFG : ", ctrl_data , "len : ", len(ctrl_data) )

    while len(ctrl_data) < 257 :    # fill up to 257 bytes
        ctrl_data.append(0x00)

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
    print "Return from report 2 - COMPLETE : " ,"\n " , ret 




#       ***         Setup USB HID connection



all_dev = usb.core.find(find_all=True)

for dev in all_dev:
    print("  Vend: ", dev.idVendor, "  prod: ", dev.idProduct )

# printout : Airbar HID : ('\tVend: ', 5430, '\tprod: ', 257)
dev = usb.core.find(idVendor=5430, idProduct=257 )   #24867

if dev:
    
    # * Connecting

    print(" Got the HID device !")
    print "Dev :\t  Len ", dev.bLength, ", Num conf ", dev.bNumConfigurations, " , dev class ", dev.bDeviceClass 
    # print "Config : \n" + str(cfg.bConfigurationValue) , " :: " + str(dir(cfg)) 
    # print " \n \t config [ " + str(dir( cfg.bConfigurationValue)) + " ] "
    interface = 0
    endpoint = dev[0][(0,0)][0]
    #print("Endpoint : ", endpoint)
    #print("Attributes : ", endpoint.bmAttributes)
    if dev.is_kernel_driver_active(interface) is True:
        dev.detach_kernel_driver(interface)
        usb.util.claim_interface(dev, interface)
        print("detached USB HID from system ")
    
    print("USB HID ready")

    # *  Sending Transfer 

    print("Sending neonode config setup ")
    cfg_data = [ 0xEE, 0x09, 0x40, 0x02, 0x02, 0x00, 0x73, 0x03, 0x86, 0x01, 0x05 ] 
    airbar_send_config( cfg_data )

    # * Lets Begin 
    print(" \nLet's begin \n")

    touching = False

    while True:
        timeout = 11
        try:
            data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize, timeout )
            # print( "HID read : " , len(data)) 

            if len(data) > 2 :
                #----
                no_touches = data[1]                
                timestamp = ( data[3] <<8) +data[2]

                touches=[]
                #touches.append(timestamp)
                aix = 4 # for shifting index of touch data

                for x in range(no_touches):
                    air = {}
                    air['id'] = data[aix]    ## ID & release

                    if air['id'] % 2 is 1 :     # uneven ID = touch
                        #print "\t",  air['id'] , " is in array ",  int_in_array( air['id'], touches ) 
                        #if not int_in_array( air['id'], touches ) :
                        air['x'] = ( data[aix+2] <<8) +data[aix+1]
                        air['y'] = ( data[aix+4] <<8) +data[aix+3]
                        air['s'] = data[aix+5] + (data[aix+6]<<8)
                    touches.append( air) 
                    aix += 9

                if socketIO:
                    socketIO.emit('airbar', touches )

                if True:    
                    # * print touches dic
                    for dic in touches:
                        print str(dic ), "\t ",
                    print "."

                if False:
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
            #sleep(0.005)
        except usb.core.USBError as e:
            print( e)
            e = ""



#--