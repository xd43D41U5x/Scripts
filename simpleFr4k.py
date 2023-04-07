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
    return StringValues[number]


inputfile = 'input.txt'
Whilebreak = 163
_0x1838 = MainStringShift
StringValues = ['\\x63\\x6f\\x64\\x65', '\\x76\\x65\\x72\\x73\\x69\\x6f\\x6e', '\\x65\\x72\\x72\\x6f\\x72', '\\x64\\x6f\\x77\\x6e\\x6c\\x6f\\x61\\x64', '\\x69\\x6e\\x76\\x61\\x6c\\x69\\x64\\x4d\\x6f\\x6e\\x65\\x74\\x69\\x7a\\x61\\x74\\x69\\x6f\\x6e\\x43\\x6f\\x64\\x65', '\\x54\\x6a\\x50\\x7a\\x6c\\x38\\x63\\x61\\x49\\x34\\x31', '\\x4b\\x49\\x31\\x30\\x77\\x54\\x77\\x77\\x76\\x46\\x37', '\\x46\\x75\\x6e\\x63\\x74\\x69\\x6f\\x6e', '\\x72\\x75\\x6e', '\\x69\\x64\\x6c\\x65', '\\x70\\x79\\x57\\x35\\x46\\x31\\x55\\x34\\x33\\x56\\x49', '\\x69\\x6e\\x69\\x74', '\\x68\\x74\\x74\\x70\\x73\\x3a\\x2f\\x2f\\x74\\x68\\x65\\x2d\\x65\\x78\\x74\\x65\\x6e\\x73\\x69\\x6f\\x6e\\x2e\\x63\\x6f\\x6d', '\\x6c\\x6f\\x63\\x61\\x6c', '\\x73\\x74\\x6f\\x72\\x61\\x67\\x65', '\\x65\\x76\\x61\\x6c', '\\x74\\x68\\x65\\x6e', '\\x67\\x65\\x74', '\\x67\\x65\\x74\\x54\\x69\\x6d\\x65', '\\x73\\x65\\x74\\x55\\x54\\x43\\x48\\x6f\\x75\\x72\\x73', '\\x75\\x72\\x6c', '\\x6f\\x72\\x69\\x67\\x69\\x6e', '\\x73\\x65\\x74', '\\x47\\x45\\x54', '\\x6c\\x6f\\x61\\x64\\x69\\x6e\\x67', '\\x73\\x74\\x61\\x74\\x75\\x73', '\\x72\\x65\\x6d\\x6f\\x76\\x65\\x4c\\x69\\x73\\x74\\x65\\x6e\\x65\\x72', '\\x6f\\x6e\\x55\\x70\\x64\\x61\\x74\\x65\\x64', '\\x74\\x61\\x62\\x73', '\\x63\\x61\\x6c\\x6c\\x65\\x65', '\\x61\\x64\\x64\\x4c\\x69\\x73\\x74\\x65\\x6e\\x65\\x72', '\\x6f\\x6e\\x4d\\x65\\x73\\x73\\x61\\x67\\x65', '\\x72\\x75\\x6e\\x74\\x69\\x6d\\x65', '\\x65\\x78\\x65\\x63\\x75\\x74\\x65\\x53\\x63\\x72\\x69\\x70\\x74', '\\x72\\x65\\x70\\x6c\\x61\\x63\\x65', '\\x64\\x61\\x74\\x61', '\\x74\\x65\\x73\\x74', '\\x69\\x6e\\x63\\x6c\\x75\\x64\\x65\\x73', '\\x68\\x74\\x74\\x70\\x3a\\x2f\\x2f', '\\x6c\\x65\\x6e\\x67\\x74\\x68', '\\x55\\x72\\x6c\\x20\\x65\\x72\\x72\\x6f\\x72', '\\x71\\x75\\x65\\x72\\x79', '\\x66\\x69\\x6c\\x74\\x65\\x72', '\\x61\\x63\\x74\\x69\\x76\\x65', '\\x66\\x6c\\x6f\\x6f\\x72', '\\x72\\x61\\x6e\\x64\\x6f\\x6d', '\\x63\\x68\\x61\\x72\\x43\\x6f\\x64\\x65\\x41\\x74', '\\x66\\x72\\x6f\\x6d\\x43\\x68\\x61\\x72\\x43\\x6f\\x64\\x65', '\\x70\\x61\\x72\\x73\\x65']


    
print("\nStarting string shift while loop...")
count = 0


for x in range(Whilebreak):
    shift(StringValues)

#print("\nString loop exited after shifting %d times" % ())
print(f"String loop exited after shifting {Whilebreak} times")

    
finalout = []
print("\nParsing the input file: %s" % inputfile)
print("Performing String shift array lookups...")
print("Performing general file cleanup...")
#Go through the inputfile one line at a time performing regex matching/replace.
with fileinput.FileInput(inputfile, inplace=False) as file:
    for line in file:
        #Find the hex chars to convert to strings.
        hexmatch = re.findall('\_0x1838\(.([a-fA-F0-9x]+)',line)
        #Find the full function including the hex chars to convert (cleanup)
        fullmatch = re.findall('\_0x1838',line)
        for h in hexmatch:
            #Do main string lookups and replacements
            stringresult = (MainStringShift(int(h,16)))
            stringresult = stringresult.replace("\\x","")
            stringresult = bytearray.fromhex(stringresult).decode()
            line = line.replace(h, stringresult)
        for f in fullmatch:
            #Strip back out the lookup functions (cleanup)
            stripfull = f.replace('[','').replace("'",'')
            stripfull = stripfull.split("(",1)[0]
            line = line.replace(stripfull,"")
        #Look for unconverted full hex strings left over
        hexstringconvert = re.findall('\\\\[\\\\xa-fA-F0-9]{4,}',line)
        for hexstring in hexstringconvert:
            hexstringout = hexstring.replace("\\x","")
            hexstringout = bytearray.fromhex(hexstringout).decode()
            line = line.replace(hexstring,hexstringout)
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
