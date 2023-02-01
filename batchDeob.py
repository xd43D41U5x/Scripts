from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import fileinput
import base64
import zlib
import re

batFile = input("Enter batch file name: ")

#go through obfuscated batch file one line at a time looking for split variables, add to a dict if found.
result = []
varDictLookup = {}
print("Finding all possible variables and creating dictionary...")
with fileinput.FileInput(batFile, inplace=False) as file:
    for line in file:
        varMatch = re.findall('%[\w\d]+%"([^\n]+)',line)
        if varMatch:
            for v in varMatch:
                temp = v.split('=',1)
                try:
                    varDictLookup.update({temp[0]:temp[1].strip('"')})
                except:
                    print(f"Skipped potential variable {v}")

#We have to go back through the same file because the dictionary needs to be fully created first.
print('Performing var replacement and concat...')
codeOut = []

with fileinput.FileInput(batFile, inplace=False) as file:
    for line in file:
        encryptedBlock = re.findall('[\:]{2}.{30,}[^\n]+',line)
        if encryptedBlock:
            print('Encrypted code block found...')
            encOut = encryptedBlock[0]
        codeBlockMatch = re.findall('%[\w\d]+%{2}[^\n]+',line)
        if codeBlockMatch:
            for c in codeBlockMatch:
                tempCode = c.split('%%')
                output = ""
                for t in tempCode:
                    t = t.strip('%')
                    output += varDictLookup[t]
                codeOut.append(output)
        
        

print("Final Code Blocks decoded: \n")
count = 1
for c in codeOut:
    print(f'{count}. {c}')
    count += 1

#Attempt to find the key and iv, then decypt.
if encOut:
    print('Previous encrypted block found, attempting AES decrypt.')
    for code in codeOut:
        if 'key' in code.lower():
            print("Code containing a key found, proceeding...")
            keyMatch = re.findall('key.*?\(\'([\w\d\+\/\=]{20,})',code, flags=re.IGNORECASE)
            ivMatch = re.findall('iv.*?\(\'([\w\d\+\/\=]{20,})',code, flags=re.IGNORECASE)

if keyMatch and ivMatch:
    #Format and convert base64 values to bytes
    encOut = encOut.strip('::').strip()
    encBytes = base64.b64decode(encOut)
    keyBytes = base64.b64decode(keyMatch[0])
    ivBytes = base64.b64decode(ivMatch[0])

    #AES Decrypt
    cipher = Cipher(algorithms.AES(keyBytes), modes.CBC(ivBytes))
    decryptor = cipher.decryptor()
    out = decryptor.update(encBytes) + decryptor.finalize()

    #Check for 
    gzipCheck = out.hex()
    if '1f8b' == gzipCheck[:4]:
        print('Gzip file found, decompressing...')
        gzipout = zlib.decompress(out,15+32)
        with open('outFileUnzip.txt',"wb") as outfile:
            outfile.write(gzipout)
    else:
        print('No compression found, writing out raw file...')
        with open('outFile.txt',"wb") as outfile:
            outfile.write(out)

else:
    print('No key and/or iv found, review returned code blocks.')
