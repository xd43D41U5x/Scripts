import re
import fileinput
import time

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

def MainStringShift(number):
    if (isinstance(number, str)):
        number = int(number,16)
    return StringValues[number-PosShift]

#Values Created from main script.
inputfile = InsertInputFile
PosShift = InsertPosShift
Whilebreak = InsertWhileBreak
InsertMainStringShiftVar = MainStringShift
StringValues = InsertStringValues


agres = input("Attempt agressive pattern matching? (Note: this could produce anomalous results, check code first): ")

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
        ###Only update the "tryfun" variable with the math seen in your code example.
        tryfun = InsertWhileLoopValue
        if (tryfun == int(Whilebreak)):
            break
        else:
            shift(StringValues)
    except:
        shift(StringValues)


###End User value input section, do not change anything outside of this section.
########################

print("\nString loop exited after shifting %d times" % (count-1))

    
finalout = []
print("\nParsing the input file: %s" % inputfile)
print("Performing String shift array lookups...")
print("Performing general file cleanup...")
#Go through the inputfile one line at a time performing regex matching/replace.
with fileinput.FileInput(inputfile, inplace=False) as file:
    for line in file:
        #Find the hex chars to convert to strings.
        hexmatch = re.findall('(?:[\(])0x[a-zA-Z0-9]+(?:[\)])',line)
        #Find the full function including the hex chars to convert (cleanup)
        fullmatch = re.findall('_0x[a-zA-Z0-9]+\(0x[a-zA-Z0-9]+',line)
        #Find the left over null/not used functions (cleanup)
        nullfun = re.findall('var\s\_0x[a-zA-Z0-9]+\s\=\s\_0x[a-zA-Z0-9]+\;',line)
        for h in hexmatch:
            hexconvert = h.replace('(','').replace(')','')
            stringresult = (MainStringShift(int(hexconvert,16)))
            line = line.replace(hexconvert, stringresult)
        for f in fullmatch:
            stripfull = f.replace('[','').replace("'",'')
            stripfull = stripfull.split("(",1)[0]
            line = line.replace(stripfull,"")
        for n in nullfun:
            line = line.replace(n,"")
        if (agres == "y"):
            agresmatch = re.findall('\_0x[a-fA-F0-9]+\((0x[a-fA-F0-9]+)',line)
            for a in agresmatch:
                agresresult = (MainStringShift(int(agresmatch,16)))
                line = line.replace(agresmatch, agresresult)
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
print("Output file saved as: %s" % outputfile)
with open(outputfile, 'w') as f:
    for final in finalout:
        f.write(final)
      






