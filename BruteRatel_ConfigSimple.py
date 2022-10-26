#Will search decoded brute ratel updater payload, find and decrypt the config
#This is a stripped down version of "full" in which you already have a decrypted shellcode payload.

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import binascii
import base64
import sys
import re

#read in a small portion of the file
fileName = input("Enter file name: ")
with open(fileName, "rb") as f:
            f.seek(400)
            fileBytes = f.read(700)

#convert to ascii to search for strings                    
asciiBytes =  "".join( chr(x) for x in fileBytes)

#search for known config pattern on disk
config = re.search('(([a-zA-Z0-9\/\=\+]{4,10})\¸*){20,}',asciiBytes)

if(config == None):
    print(f'Config not found')
    sys.exit()
else:
    print(f'Config found, proceeding...\n')
    
#split and reorder
configList = config.group(0).split('¸')
configList.reverse()

#stip trailing bytes not needed
out = []
for x in configList:
    out.append(x[:-2])

#rejoin into a string
finalConfig = "".join(out)

#b64 decode
b64Decode = base64.b64decode(finalConfig)

#RC4 decrypt
key = str.encode('bYXJm/3#M?:XyMBF')
keyAns = input("Would you like to change the default key from 'bYXJm/3#M?:XyMBF'? ")
if(keyAns.lower() == 'y'):
    newKey = input("What is the new key: ")
    key = str.encode(newKey)
else:
    print(f'\nUsing default/known key to decrypt.\n')

algorithm = algorithms.ARC4(key)
cipher = Cipher(algorithm, mode=None)
decryptor = cipher.decryptor()
decryptedConfig = decryptor.update(b64Decode)
formatDecConfig = decryptedConfig.decode('utf-8')

print(f'The full decrypted config is: \n\n{formatDecConfig}\n')

formatDecConfig = formatDecConfig.split("|")

print(f'Pretty Print Config:\n')
for f in formatDecConfig:
    if (f != ""):
        if ("=" in f):
            try:
                print((base64.b64decode(f)).decode('utf-8'))
            except:
                print(f)
        else:
            print(f)
