import fileinput
import re

inputfile = 'input.txt'

ac = ["string1","string2","string3"]

regmatch = '\_ac\[[0-9]+\]'
stringvar = '_ac'

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
            stripfull = f.replace('[','').replace(stringvar,'').replace(']','')
            #replace each match with the new lookup/cleaned value
            line = line.replace(f,ac[int(stripfull)])
        #Add the new line for output
        finalout.append(line)

print("\nDecode finished...")

outputfile = inputfile+".out"
print("Output file saved as: %s" % outputfile)
with open(outputfile, 'w') as f:
    for final in finalout:
        f.write(final)
