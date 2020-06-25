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

socket_disable = True

import usb.core
import usb.util
import sys
import math
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
    socketIO.emit('msg', 'Hey. Its me, airbar. ')
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
        serverName = 'localhost'  # 'MUL00175'     'nodeserver'   '192.168.86.127'
        serverPort = 8000
        print "Connecting socket ", serverName, ":", serverPort
        self.socket = SocketIO(serverName, serverPort, LoggingNamespace)
        self.socket.on('connect', on_connect)
        self.socket.on('disconnect', on_disconnect)
        self.socket.on('reconnect', on_reconnect)
        self.socket.on('msg', socket_msg )


def thread_client(socketThr):
    socketThr.wait()

socketIO = None
if not socket_disable:
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



def airbar_loop():
    first_touch = True
        
    while True:
        try:
            data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize, timeout )

            if len(data) > 2 :
                
                # ** SEND TOUCHES

                no_touches = data[1]                
                timestamp = ( data[3] <<8) +data[2]
                touches=[ no_touches, timestamp ]

                aix = 4 # for shifting index of touch data
                for x in range(no_touches):
                    air = []
                    air.append(data[aix])    # 'id' = 0

                    if air[0] % 2 is 1 :     # uneven ID = touch
                        air.append( ( data[aix+2] <<8) +data[aix+1] )   # 'x' = 1
                        air.append( ( data[aix+4] <<8) +data[aix+3] )   # 'y' = 2
                        air.append( data[aix+5] + (data[aix+6]<<8) )    # 's' = 3
                    touches.append( air) 
                    aix += 9

                if no_touches > 0:
                    # ** Send via Socket
                    # if socketIO:                            socketIO.emit('airbar', touches )
                    if first_touch:
                    	airbar_begin(touches)
                    	first_touch = False
                    else:
                    	airbar_touch( touches )

                # release
                if no_touches is 1 and data[4]%2==0:
                    first_touch = True
                
            #sleep(0.005)
        except usb.core.USBError as e:
            # print e
            e = ""

class Touch:
	def __init__(self, id ):
		self.id = id
		self.x = 0
		self.y = 0
		self.px = 0
		self.py = 0
		self.dx = 0
		self.dy = 0
		self.totalx = 0
		self.totaly = 0

touches = {}
one_finger = { 'pan': [0,0] }
two_finger = { }
fingers = []

def airbar_begin(data):
	global one_finger, two_finger

	one_finger['pan'] = [0,0]
	two_finger['pan'] = [0,0]

	for x in range(data[0]):
		touch = data[2+x]
		id = touch[0]
		touches[id] = Touch(id) # key 
		touches[id].px = touch[1]
		touches[id].py = touch[2]

	print 'Begin ' 



def airbar_touch(data):
	global fingers

	# print 'touch data \t', data 

	for x in range(data[0]):
		touch = data[2+x]
		id = touch[0]
		if id%2 ==0 :
			id+=1
			# even : release
			# remove from touches
			if (id) in touches:
				touches.pop(id)	
		else:
			# odd : touch
			if id not in touches:
				# add if new
				touches[id] = Touch(id)
				touches[id].px = touch[1]
				touches[id].py = touch[2]

			# update touch object
			touches[id].x = touch[1]
			touches[id].y = touch[2]
			touches[id].dx = touches[id].x-touches[id].px
			touches[id].dy = touches[id].y-touches[id].py
			touches[id].totalx += touches[id].dx 
			touches[id].totaly += touches[id].dy
			touches[id].px = touches[id].x
			touches[id].py = touches[id].y

	# check change of fingers
	finger_change = not check_fingers(fingers,touches)
	
	# update fingers array
	fingers=[]
	for touch in touches.values():
		fingers.append(touch.id)

	# run gesture recognition
	gestures(touches,finger_change)

	if len(touches) == 0:
		print ' release '

def airbar_release(data):
	# if socketIO: # 	socketIO.emit('airbar', [0, 'release'] )
	print ' release ', data 

def check_fingers(fingers,touches):
	identical = True
	if len(touches) != len(fingers):
		identical = False
	else:
		for f in fingers:
			if f not in touches:
				identical = False
	return identical


def gestures(touches, change):
	global one_finger, two_finger

	L = len(touches)
	if L is 1:		
		# - - - - - pan
		touch = touches.values()[0]
		one_finger['pan'][0] += touch.dx
		one_finger['pan'][1] += touch.dy

		print ' one finger :  pan ', [touch.dx, touch.dy], '\t > ',  one_finger['pan']

	elif L is 2:
		
		A = touches.values()[0]
		B = touches.values()[1]
		
		if change:
			# first time two fingers / different fingers
			print '\t# #  reset ! '
			two_finger['pan'] = [0,0]
			touches.values()[0].totalx = 0
			touches.values()[0].totaly = 0
			touches.values()[1].totalx = 0
			touches.values()[1].totaly = 0

		# * total diff
		# print ' two_finger : ', [A.x, A.y], [B.x,B.y] 
		dist = abs( A.x-B.x) + abs(A.y-B.y)
		diff = [A.totalx-B.totalx , A.totaly-B.totaly ]
		if A.totalx != 0 and A.totaly != 0 :
			# compare magnitudes ?
			ratio = 0.0 * ( abs(diff[0])+abs(diff[1]) ) / ( abs(A.totalx) + abs(A.totaly) )

			print ' total diff ', diff 
			

		# * by angle
		a = math.atan2(A.dx,A.dy)
		b = math.atan2(B.dx,B.dy)
		angleDiff = math.floor( (a-b)*1000) / 1000
		# if angleDiff > 0.3:
		# 	print ' Two finger : \t diff ', '\t : ', angleDiff	
		

		#print ' Two finger : \t diff ', '\t : ', angleDiff

		#print [ A.dx,A.dy] , [B.dx,B.dy]
		#print [ A.totalx, A.totaly ], [B.totalx, B.totaly], diff
		

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
    # config 1 : 5 touches
    cfg_data = [ 0xEE, 0x09, 0x40, 0x02, 0x02, 0x00, 0x73, 0x03, 0x86, 0x01, 0x05 ] 
    airbar_send_config( cfg_data )

    # * Lets Begin 
    print(" \nRight now, let's begin \n")

    timeout = 11
    
    airbar_loop()
else:
	print(' no matching HID device found ')




#--