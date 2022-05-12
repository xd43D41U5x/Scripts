import re
import fileinput
import time
import sys

#########Function Import Section Start#########

InsertFunctionSection

#########Function Import Section End#########

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
      

