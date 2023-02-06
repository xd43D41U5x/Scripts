#Recent obfuscation that starts with an escaped string and then multiple rounds of similar nested powershell code.
#Pattern is b64 > powershell script with minor obfuscation and more b64 > b64 and gzip file.
#In the testing case for this script it was 8 total rounds, which takes time by hand.
from io import BytesIO
import base64
import gzip
import re

def unescape(uString):
    out = uString.replace('%','')
    byte_out = bytearray.fromhex(out)
    return byte_out.decode()

def findB64(bString):
    out = ""
    try:
        bString = bString.decode('ascii')
    except:
        pass
    bFind = re.findall('[\w+\/=]{20,}',bString)
    if bFind:
        out = bFind[0]
        if not (len(out)%4) == 0:
            while not (len(out)%4) == 0:
                out += '='
    return out

def unGzip(data):
    filebytes = BytesIO(data)
    with gzip.open(filebytes,'rb') as f:
        file_content = f.read()
    return file_content
                
#Enter escapted string here
eString = ''''''

uString = unescape(eString)
count = 0
while True:
    b64Test = re.findall('[\w+\/=]{20,}',uString)

    if b64Test:
        count += 1
        b64Results = findB64(uString)
        bOut = base64.b64decode(b64Results)
        try:
            bOut = bOut.decode('utf-8').replace('\x00','')
            uString = bOut
        except:
            gZipTest = re.findall('1f8b',bOut.hex()[:4])
            if gZipTest:
                gOut = unGzip(bOut)
            uString = gOut.decode('utf-8').replace('\x00','')
    else:
        print(f'Finished unpacking/decode after {count} rounds, output:\n{uString}')
        input("Press any key to exit...")
        break
