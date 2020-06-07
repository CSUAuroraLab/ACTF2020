from binascii import hexlify,unhexlify

def hexpad(hexBlock):
    numZeros = 8 - len(hexBlock)
    return numZeros*"0" + hexBlock
   
def substitute(hexBlock):
    substitutedHexBlock = ""
    substitution = [15, 9, 7, 4, 1, 11, 6, 10, 0, 3, 13, 14, 12, 8, 5, 2]
    for hexDigit in hexBlock:
        newDigit = substitution[int(hexDigit, 16)]
        substitutedHexBlock += hex(newDigit)[2:]
   
    return substitutedHexBlock
   
   
def permute(hexBlock):
    permutation =   [6, 22, 30, 18, 29, 4, 23, 19, 15, 1, 31, 11, 28, 14, 25, 2, 27, 12, 21, 26, 10, 16, 0, 24, 7, 5, 3, 20, 13, 9, 17, 8]
    sub_block = ["0" for i in range(32)]
    for i in range(31, -1, -1):
        enc_block = format(int(hexBlock, 16), "032b")
   
        if enc_block[i] == "1": 
            bit = permutation.index(31 - i)
            sub_block[bit] = "1"
           
    sub_block = "".join(sub_block[::-1])
   
    return hexpad(hex(int(sub_block, 2))[2:])
   
   
def round(hexMessage):
    numBlocks = len(hexMessage)//8
    permutedHexMessage = ""
    for i in range(numBlocks):
        permutedHexMessage += permute(hexMessage[8*i:8*i+8])
    substitutedHexMessage = ""
    for i in range(numBlocks):
        substitutedHexMessage += substitute(permutedHexMessage[8*i:8*i+8])
    return substitutedHexMessage
   
   
if __name__ == "__main__":
   
    with open("cipher.txt", "r") as ciphertext:
        hexMessage = ciphertext.read()
        for i in range(10000):
            hexMessage = round(hexMessage)
    print(unhexlify(hexMessage).decode("utf-8"))
     
