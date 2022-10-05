from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from subprocess import check_output
import binascii
import hashlib

def bitDecrypt(value,datVal,magic):
    #input string value to checksum
    value = p + magic
    pad = 0xFFFFFFFF

    print(f'Using the hardcoded string value: {value}')

    #encrypted info
    datVal = bytes.fromhex(posEnc[0])

    print(f'Using encrypted data starting with {datVal[:16].hex()} and a length of {len(datVal)} bytes.')

    #calc crc32 checksum of hardcoded string value
    crc32Output = binascii.crc32(str.encode(value))
    crc32Offset = (crc32Output&pad)+8
    print(f'The checksum value is: {hex(crc32Offset)}')

    #format and MD5 hash the crc32 result
    hashFormat = f'{crc32Offset:x}'
    finalHash = hashlib.md5(hashFormat.encode('utf8')).hexdigest()
    print(f'The MD5 hash is: {finalHash}')

    #split hash and take first 16
    decryptKey = finalHash[0:16]
    print(f'The decrypt key is: {decryptKey}')

    #format the key and IV
    key = str.encode(decryptKey)
    iv = "00000000000000000000000000000000"
    iv = bytes.fromhex(iv)

    #Selct Cipher with key and mode
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))

    #decrypt
    decryptor = cipher.decryptor()
    out = decryptor.update(datVal) + decryptor.finalize()

    return out

def findMagic(enc):
    magic = ""
    for s in range(0,len(enc),2):
        val = int(enc[s:s+2],16)
        res = (((((val - 0x8)*0x25))%0x7f)+0x7f)%0x7f
        magic += chr(res)
    return magic

#prompt and update the magic value then decode if needed
prompt = input('Typically the starting magic value is 78hf326f87 based on encoded strings of 553D3464364E6D643D55. Do you need to change this value y/n: ')
if (str.lower(prompt) == 'n'):
    magic = "78hf326f87"
else:
    mnum = input('Enter new magic value: ')
    magic = findMagic(mnum)

#Search file for key data values
#first attempt to find the starting key magic value
fileName = input('What is the filename: ')
findKey = 'strings -n 16 '+ fileName + ' | grep -E "^[a-fA-F0-9]{16}$"'
posKey = check_output(findKey, shell=True).decode()
posKey = posKey.strip().split('\n')
#dedup
keyList = [*set(posKey)]

#next try to find the encrypted data
findEncData = 'strings -n 7 ' + fileName + ' | grep -E "^[^4d5a][a-fA-F0-9]{50,}$"'''
posEnc = check_output(findEncData, shell=True).decode()
posEnc = posEnc.split(' ')

#main loop to try the found values.  If multiple possible magic key values, attempt to brute force
if len(posEnc) == 1:
    if len(keyList) == 1:
        out = bitDecrypt(keyList,posEnc,magic)
        print(f'The decrypted config is:\n{out.decode()}')
    else:
        print(f'Multiple possible keys found, attempting brute force...\n')
        for p in keyList:
            try:
                out = bitDecrypt(p,posEnc,magic)
                print(f'The decrypted config is:\n{out.decode()}')
                break
            except:
                print('Decrypt failed with given key, attempting next one...\n\n')
else:
    print(f'Multiple possible values found ({len(posEnc)})review:\n')
    for o in range(len(posEnc)):
        print(f'{o} - {posEnc[o]}')
