##!/usr/bin/python

"""
	use this to get first data out, looking at data frame

'B'		3	1	V1	V2		IDT    A1 A2 

 - V1 V2 change wildly...
 - IDT =    += X for new touch ,       then -1 on release

"""

# ------------		SOCKET
import thread, logging
from socketIO_client import SocketIO, LoggingNamespace
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

NO_CONSOLE = True

def on_connect():
    global socketReady
    socketReady = True
    print ("Connected to server!!!")
    print ("commsReady "+str(socketReady))

def on_disconnect():
    print ("disconnected from server")

def on_reconnect():
    print ("reconnected to server")

def socket_ping(*args):
	print "Socket Pinggg! : ", args

def socket_msg(*args):
	print(" # Socket msg : ", args)


class NetConn():
    socket = None
    def __init__(self):
        serverName = 'touchpadpi'
        serverPort = 3000
        print "Connecting socket ", serverName, ":", serverPort
        self.socket = SocketIO(serverName, serverPort, LoggingNamespace)
        self.socket.on('connect', on_connect)
        self.socket.on('disconnect', on_disconnect)
        self.socket.on('reconnect', on_reconnect)
        self.socket.on('ping', socket_ping)
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
except:
    print " # # Thread error."

# ------------ 		USB


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

        while True:
        	try:
	        	data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize, 10)
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

	        	if socketIO:
	        		#socketIO.emit('touch', [ 'touch',air['x1'], air['y1'] ] )
	        		if air['id1'] & 0x01 :
	        			socketIO.emit('touch', air )
	        		else:
	        			socketIO.emit('release' , 1)

	        	
	        	if False:
	        		# Print array
	        		#print data
	        		for x in range(0, 20):		#len(data) ):
	        			print data[x],"\t",
	        		print " .", len(data)
	        	
	        	if False:
	        		# Print dict
		        	for tag in air:
		        		print tag ,": ", air[tag], "\t",
		        	print "."
		        	#print bin(data[4])		# ID + Touch

		        if not NO_CONSOLE :
		        	print "Touch ", air['id1'] , ":\t", air['x1'], " ,\t", air['y1'], "\tS( ", air['s1'], ")"	# &0x03

        	except usb.core.USBError as e:
		        #print( e)
		        new_error = e

	#--