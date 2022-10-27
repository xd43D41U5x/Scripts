#Will take given Brute Ratel dll and encrypted shellcode from the ISO
##Find the key and XOR decrypt the shellcode
###Decode the shellcode and convert to a dll in a similar manner it does (moves dll in byte chunks onto stack)
####Find Config and RC4 key, then decrypt

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from subprocess import check_output
import binascii
import base64
import sys
import re

def xor(data, key):
    l = len(key)
    #standard xor for multibyte key with data
    return(bytearray(((data[i] ^ key[i % l]) for i in range(0,len(data)))))

def decryptRC4(data,key):
    algorithm = algorithms.ARC4(key)
    cipher = Cipher(algorithm, mode=None)
    decryptor = cipher.decryptor()
    decryptedConfig = decryptor.update(data)
    return(decryptedConfig.decode('utf-8'))

def shellConvert(shell):
    #Convert to hex to look for opcodes
    hexDataShell = bytearray(shell).hex()
    #Look for known shellcode opcodes related to this sample.
    findPushesShell = re.findall(r'(?:48)?((b8[a-z0-9]{8})|(b8[a-z0-9]{16}))(?:50)',hexDataShell)
    out = ""
    #Loop through found opcodes and mimic to rebuild the dll
    for f in findPushesShell:
        f = f[0]
        if len(f[2:]) != 8 and len(f[2:]) !=16:
            print(f"The length of data is off, review file and try again...\nExample: {f}")
            sys.exit()
        #strip stack push and rebuild
        out = f[2:] + out
    #return bytes to write to file
    return(bytes.fromhex(out))

def sysCmd(cmd):
    return(check_output(cmd, shell=True).decode())

def openFile(fileName):
    with open(fileName, "rb") as f:
        fileBytes = f.read()
    return fileBytes

def writeFile(fileName,fileBytes):
    with open(fileName, "wb") as binaryFile:
        binaryFile.write(fileBytes)
    print(f'File written successfully as: {fileName}')



#######MAIN#######


fileNameDll = input("Enter dll file name: ")
fileNameBadger = input("Enter Encrypted Updater file name: ")
#fileNameDll = 'version.dll'
#fileNameBadger = 'OneDrive.Update'

fileBytesDll = openFile(fileNameDll)

posXORKey = sysCmd('strings -10 ' + fileNameDll)

#Grabbing the XOR key from a known portion of the code.
posXORKey = posXORKey.split('Please wait...\n')[1]
posXORKey = posXORKey.split('\n')[0]
print(f'Possible XOR key found!\nKey: {posXORKey}')

xAnswer = input('Would you like to override this found key? ')
if (xAnswer.lower() == 'y'):
    posXORKey = input('Please input new XOR key: ')


fileBytesBadger = openFile(fileNameBadger)

bytesKey = str.encode(posXORKey)

xorResults = xor(fileBytesBadger,bytesKey)

shellBytes = shellConvert(xorResults)

#The file being written out here seems to vary a bit based on public samples. Sometimes you get an executable with a valid MZ header.
#Other times you get more shellcode.  Either way the way we find the key and config stays the same for now and works.
print(f'Writing out dll, remember to fix the MZ header...')
writeFile('outshell.dll',shellBytes)

#look for config in dll dump
posConfig = sysCmd('strings -50 outshell.dll')

if(posConfig):
    print(f'Config found proceeding...\nEncoded Config:\n{posConfig}')
else:
    print(f'No config found, review...')
    sys.exit()

#b64 decode
b64Config = base64.b64decode(posConfig)

#Set the standard key found across multiple samples but still look for and prompt as this could change.
stdRC4Key = 'bYXJm/3#M?:XyMBF'

#Try to confirm RC4 key
posRC4Key = sysCmd('strings -n 16 outShell.dll | sort | uniq -c | sort -rn | head -n 1')
foundRC4Key = posRC4Key.strip().split(' ')[1]

if(foundRC4Key == stdRC4Key):
    print(f'Found and confirmed standard key of "{stdRC4Key}", proceeding to use this...')
    key = str.encode(stdRC4Key)
else:
    newKey = input(f'Key not found, would you still like to attempt the standard key of: {stdRC4Key}? ')
    if(keyAns.lower() == 'n'):
        newKey = input("What is the new key?: ")
        key = str.encode(newKey)
    else:
        print(f'\nUsing default/known key to decrypt.\n')
    

#Dectypt with RC4
decryptedConfig = decryptRC4(b64Config,key)

print(f'\nThe full decrypted config is: \n{decryptedConfig}\n')

#Format config for easier reading and b64 decode some values.
decryptedConfig = decryptedConfig.split("|")

print(f'Pretty Print Config:\n')
for f in decryptedConfig:
    if (f != ""):
        if ("=" in f):
            try:
                print((base64.b64decode(f)).decode('utf-8'))
            except:
                print(f)
        else:
            print(f)
