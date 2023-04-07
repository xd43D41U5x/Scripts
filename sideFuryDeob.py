import fileinput
import re
import collections
import sys

def Decode(strin):
    b64 = "lfsjvHQne8xPyYUtoBMLg1bNSqmOXDpEiJuA3cK06F7TV4ZWdRzkG52wrhIaC9+/="
    result = ""
    i = r1 = r2 = 0
    
    while True:
        
        b = b64.index(strin[i]) << 18;i+=1
        b = b | b64.index(strin[i]) << 12;i+=1
        r1=b64.index(strin[i]);i+=1
        r2=b64.index(strin[i])
        b = b | r1 << 6 | r2
        i+=1
        
        if (r1 == 64):
            result += ''.join(map(chr, [b >> 16 & 255]))
        elif (r2 == 64):
            result += ''.join(map(chr, [b >> 16 & 255, b >> 8 & 255]))
        else:
            result += ''.join(map(chr, [b >> 16 & 255, b >> 8 & 255, b & 255]))
        if (i >= len(strin)):
            break
    return result


def Decrypt(key,byte):
    res = []
    i = 0
    
    while(i<len(byte)):
        j = 0
        while(j<len(key)):
            res.insert(0,''.join(map(chr,[ord(byte[i]) ^ ord(key[j]) ^ i % 3])))
            i+=1
            
            if (i >= len(byte)):
                break
            j+=1
    return ''.join(res)


def MainDecode(b):
    key = Decrypt("bWqQ",Decode("gQ1"+"PYH"+"8iB"+"jS="))
    return Decrypt(key,Decode(b))


def freqfinder(inputfile):
    freqmatch = '\w+\('

    fullmatch2 = []
    
    with fileinput.FileInput(inputfile, inplace=False) as file:
        for line in file:
            fullmatch2 += re.findall(freqmatch,line)

    newfull = []
    for full in fullmatch2:
        new_full = full.replace('(','')
        newfull.append(new_full)

    occur = collections.Counter(newfull).most_common(3)
    for o in occur:
        print("Possible Function: {} - Count: {}".format(o[0],o[1]))


freqcheck = input("Would you like to perform freq analysis and determine possible decode fucntions? (Y/N): ")

inputfile = 'obfile.txt'

regmatch = 'vezbFYuv\([^\)]*\)'
stringvar = 'vezbFYuv'

if (freqcheck.lower() == "y"):
    freqfinder(inputfile)
    sys.exit()


finalout = []

print("Starting deob with String list as variable %s, and using the regex: %s" % (stringvar,regmatch))

#Go through the inputfile one line at a time performing regex matching/replace.
with fileinput.FileInput(inputfile, inplace=False) as file:
    for line in file:
        #Find the String replacement in each line.
        fullmatch = re.findall(regmatch,line)
        #For each match do the lookup and cleanup.        
        for f in fullmatch:
            #cleanup regex matches
            stripfull = f.replace('(','').replace(stringvar,'').replace(')','')
            dodecode = MainDecode(eval(stripfull))
            #replace each match with the new lookup/cleaned value
            line = line.replace(f,dodecode)
        #Add the new line for output
        finalout.append(line)

print("\nDecode finished...")

for final in finalout:
    print(final)

outputfile = inputfile+".out"
print("Output file saved as: %s" % outputfile)
with open(outputfile, 'w') as f:
    for final in finalout:
        f.write(final)

