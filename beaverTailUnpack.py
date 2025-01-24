import zlib
import base64

def upack(cData):
    test = stringExp.split("'")
    for t in test:
        if len(t)>100:
            test = zlib.decompress(base64.b64decode(t[::-1]))
    return test

stringExp = """Enter initial code here"""
count = 0

while 'http:' not in stringExp:
    stringExp = upack(stringExp).decode("utf-8")
    print("still found, running again....")   
    count += 1

print(f"Complete...this unpacked {count} times.")   
print(stringExp)
