import re
import fileinput
import time
import sys
import js2py

#########Function Import Section Start#########

InsertFunctionSection

#########Function Import Section End#########


#########Main String Decode Function Start#########
js2 = """function _0x43bd8b(_0x1eb3d1){ 
var _0x230c51 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';
                var _0x1e2624 = '',
                _0x53423d = '';
                _0x3d36ac = _0x1e2624 + _0x43bd8b;
for (var _0x129a9a = -0x4 * 0x9 + -0x1558 + 0x157c, _0xd63862, _0x3582cc, _0xdd4aff = 0x1426 + 0x1 * -0x1cbb + 0x895; _0x3582cc = _0x1eb3d1['charAt'](_0xdd4aff++); ~_0x3582cc && (_0xd63862 = _0x129a9a % (-0x12b * -0x1e + 0x2210 + -0x228b * 0x2) ? _0xd63862 * (-0x4e2 + -0xeb7 * 0x2 + -0x229 * -0x10) + _0x3582cc : _0x3582cc, _0x129a9a++ % (-0x82 * -0xd + 0x1 * -0x136b + 0x2d * 0x49)) ? _0x1e2624 += _0x3d36ac['charCodeAt'](_0xdd4aff + (0x454 * 0x1 + -0x2 * -0x114b + 0x1 * -0x26e0)) - (0x8ea + -0x23f9 * -0x1 + 0x81 * -0x59) !== -0x5 * 0x781 + 0x33b + 0x224a ? String['fromCharCode'](0x1983 + -0x685 + -0x11ff & _0xd63862 >> ( - (-0x21 * -0x7 + 0x1746 + -0x182b) * _0x129a9a & -0x4 * 0x18e + 0xd78 + 0xb9 * -0xa)) : _0x129a9a : -0x1c59 + 0xc24 + 0x1035) {
                    _0x3582cc = _0x230c51['indexOf'](_0x3582cc);
                    
                }
               
                return _0x1e2624
                 
                }"""
                
#########Main String Decode Function End#########

#Function to mimic JS parseint.  Will check for string starting with an int.
#If its a char, returns "nan", otherwise strips only decimal chars and converts.
def parseInt(stringinput):
    try:
        int(stringinput[0])
    except:
        return "NaN"
    intnum = int(re.search(r'\d+', stringinput).group())
    return intnum


#Function to mimic a push/shift in JS.  Takes string from array on the front and moves to the back.
def shift(listinput):
    listinput.append(listinput.pop(0))

def MainStringShift(number,novalue):
    if (isinstance(number, str)):
        number = int(number,16)
    return StringValues[number-PosShift]






inputfile = InsertInputFile
PosShift = InsertPosShift
Whilebreak = InsertWhileBreak
InsertMainStringShiftVar = MainStringShift
StringValues = InsertStringValues

#########New String Decode Section Start#########
#Check our string list and make sure we have some starting with a number, decode if needed.
numcount = 0
for n in StringValues:
    try:
        int(n[0])
        numcount += 1
    except:
        continue
        
if (numcount <= 1):
    print("\nString list appears to be encoded, performing decode...")
    res2 = js2py.eval_js(js2)

    output = []
    for s in StringValues:
        output.append(res2(s))
       
    StringValues = output
    
#########New String Decode Section End#########


if StringValues and Whilebreak and PosShift and inputfile:
    print("\nKey values found, proceeding...")
else:
    print("\nMissing key values, exit...")
    exit

    
print("\nStarting string shift while loop...")
count = 0



while True:
    try:
        count += 1
        tryfun = InsertWhileLoopValue
        if (tryfun == int(Whilebreak)):
            break
        else:
            shift(StringValues)
    except:
        shift(StringValues)




print("\nString loop exited after shifting %d times" % (count-1))


finalout = []
print("\nProcessing Input File: %s" % inputfile)
print("Performing String shift array lookups and following chained functions...")
print("Performing general file cleanup...")
#Go through the inputfile one line at a time performing regex matching/replace.
with fileinput.FileInput(inputfile, inplace=False) as file:
    for line in file:
        #Find the full function including the hex chars to convert
        fullmatch = re.findall('\_0x[a-zA-Z0-9]+\(\-?0x\S.+?(?=\))',line)
        #Find the left over null/not used functions (cleanup)
        nullfun = re.findall('var\s\_0x[a-zA-Z0-9]+\s\=\s\_0x[a-zA-Z0-9]+\;',line)
        for f in fullmatch:
            stripsplit = f.split("(")
            stripfunction = stripsplit[0]
            stripparams = [int(x,16) for x in stripsplit[1].split(",")]
            fulloutput = globals()[stripfunction](*stripparams)
            line = line.replace(f,fulloutput)
        for n in nullfun:
            line = line.replace(n,"")
        #Look for any left over hex values (actual nums) and convert.
        hexconvert = re.findall('[\ |\']0x[a-fA-F0-9]+',line)
        for hc in hexconvert:
            hc = hc.replace(" ","").replace("'","")
            if (isinstance(hc, str)):
                hcn = str(int(hc,16))
            else:
                hcn = str(int(hc))
            line = line.replace(hc,hcn)
        finalout.append(line)

print("\nDecode finished...")

#Write out new file
outputfile = inputfile+".out"
print("\nOutput file saved as: %s" % outputfile)
with open(outputfile, 'w') as f:
    for final in finalout:
        f.write(final)
      

