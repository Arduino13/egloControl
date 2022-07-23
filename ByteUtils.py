def reverse(bArr):
        bArr2 = bytearray()
        for x in range(0,len(bArr)):
            bArr2.append(bArr[(len(bArr)-1)-x])
        return bArr2

def xor(bArr,bArr2):
    bArr3 = bytearray()
    for i in range(0,len(bArr)):
        bArr3.append(bArr[i] ^ bArr2[i])

    return bArr3
