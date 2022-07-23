import ByteUtils
import struct
import math
import array
from Crypto.Cipher import AES

SRC = array.array('b',[0,0]).tostring()

VENDOR_ID = array.array('b',[96,1]).tostring()
SESSION = [-77,-27,-13, -50, 8, 24, -21, 121]
SESSION = array.array('b',SESSION).tostring()

ADDR = None

#seems that user and password are hardcoded and don't change over time
USER_S = "R-0C19B0"
PASS_S = "1234"

USER = bytearray(16)
PASS = bytearray(16)
USER[0:len(USER_S)]=USER_S
PASS[0:len(PASS_S)]=PASS_S

aSequenceNumber=0;

#used to create new session key
def encrypt(bArr,bArr2):
    reverse = ByteUtils.reverse(bArr)
    reverse2 = ByteUtils.reverse(bArr2)
    key = str(reverse)
    aes = (AES.new(key,AES.MODE_ECB)).encrypt(str(reverse2))
    return bytearray(aes)

#encodes value as command to change color and to turn the light off
#for now only this command is implemented
def getValue_internal(bArr,b,bArr2):
    global aSequenceNumber

    aSequenceNumber += 1 #for now has no purpose
    #added for case multiple commands need to be launched from script 

    buff = bytearray()
    buff += struct.pack('B',(aSequenceNumber & 255))
    buff += struct.pack('B',((aSequenceNumber >> 8) & 255))
    buff += struct.pack('B',((aSequenceNumber >> 16) & 255))
    buff += SRC
    buff += bArr
    buff.append(b)
    buff += VENDOR_ID
    buff += bArr2

    for x in range(len(buff),20):
        buff.append(0)

    return buff

def getValue(s,b,bArr): 
    value = bytearray(struct.pack('<i',s))
    return getValue_internal(value[0:2],b,bArr)

def progressToValue(i,i2,i3):
    if i<0:
        i = 0
    elif i > 100:
        i = 100
    return math.round(i2+(i*(i3-i2))/100)

#creates new session key
def getSessionKey(bArr4):
    bArr = USER
    bArr2 = PASS
    bArr3 = SESSION

    bArr5 = bytearray()
    bArr5 += bArr3
    bArr5 += bArr4
    return ByteUtils.reverse(encrypt(ByteUtils.xor(bArr,bArr2),bArr5))

#it doesn't really encrypt the value that's done by telinkCrypto library but it prepares data
#for encryption, it takes part of session key and part of command and puts them together
def encryptValue(bArr2,bArr3):
    bArr=ADDR

    bArr4 = bytearray()
    bArr4 += bArr[0:4]
    bArr4.append(1)
    bArr4 += bArr3[0:3]
    return bArr4

