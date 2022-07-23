# -*- coding: utf-8 -*-

from bluepy import btle
import array
import protocol
import subprocess
import sys
import threading
import ByteUtils

#set timer to break while loop for connecting
timer = threading.Timer(10,exit)
timer.start()

DEV_MAC = "a4:c1:38:68:50:1e"
DEV_MAC_INT_ARR = [164,193,56,104,80,30]
SERVICE = "00010203-0405-0607-0809-0a0b0c0d1910"
CHARACTERISTIC_LOGIN = "00010203-0405-0607-0809-0a0b0c0d1914"
CHARACTERISTIC_CONTROL = "00010203-0405-0607-0809-0a0b0c0d1912"
DEBUG = True

protocol.ADDR = ByteUtils.reverse(array.array('B', DEV_MAC_INT_ARR).tostring())
protocol.aSequenceNumber = int(sys.argv[1]) #commands need to be numbered counter is reseted when light is turned off
red = int(sys.argv[2])
green = int(sys.argv[3])
blue = int(sys.argv[4])
power_off = int(sys.argv[5])

#encoded login creditals with 'random' key, for simplicity i use fixed key
values = [12, -77, -27, -13, -50, 8, 24, -21, 121, 21, -2, 13, -100, -95, -42, 66, 50]

def debugPrint(string):
    if DEBUG:
        print(string)

#sometimes raspberry pi won't connect on first try
connected = False
while not connected:
    try:
        light = btle.Peripheral(DEV_MAC)
        connected = True
    except:
        pass

timer.cancel()

debugPrint(light.getServices()) 
service = light.getServiceByUUID(SERVICE) 

for ch in service.getCharacteristics():
    debugPrint(ch.uuid)

char = service.getCharacteristics(forUUID=CHARACTERISTIC_LOGIN)[0]
light.writeCharacteristic(char.getHandle(),array.array('b',values),withResponse=True) #send encrypted creditals to light
response = light.readCharacteristic(char.getHandle())
response = [x for x in response]

output = bytearray()
if response[0] == '\x0d':
    for i in range(1,9):
        output.append(response[i])

    to_output = [x for x in output]
    debugPrint(to_output)
else:
    print "error"

#Decodes AES key from response 
session_key = protocol.getSessionKey(output)

#sets reuquired command
if power_off == 0:
    value = protocol.getValue(30,226,array.array('b',[4,red,green,blue]).tostring())
else:
    value = protocol.getValue(30,208,array.array('b',[0]).tostring())

#encrypts command with key
en = protocol.encryptValue(session_key,value)

#light.writeCharacteristic(char.getHandle(),array.array('b',[1]),withResponse=True)
#key = light.readCharacteristic(char.getHandle())

#writes encrypted value, session key and value to files and calls process that uses telinkCrypto library to encrypt
#the final command
with open('output_encrypt.txt','w+') as f:
    for x in session_key:
        f.write(str(x))
        f.write(' ')
    f.write('\n')
    
    for x in value:
        f.write(str(x))
        f.write(' ')
    f.write('\n')

    for x in en:
        f.write(str(x))
        f.write(' ')
    f.write('\n')

subprocess.call(['./a.out'])

#load encrypted value from file
with open('en.txt','r') as f:
    x = f.read().split(',')
x[-1] = x[-1][:-1]
x_int = []
for s in x:
    x_int.append(int(s))

debugPrint(x_int)

#sends command to light
control = service.getCharacteristics(forUUID=CHARACTERISTIC_CONTROL)[0]
light.writeCharacteristic(control.getHandle(),array.array('B',x_int),withResponse=True)
debugPrint(light.readCharacteristic(control.getHandle()))

light.disconnect()
