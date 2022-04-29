#PowerShell Scratch - small effort to obfuscate in less of a PS and more JS.
#This is to learn string list deob and reversing simple ob.
import fileinput
import re
import random
from string import ascii_letters

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def ranstring():
    return ''.join([random.choice(ascii_letters) for i in range(random.randrange(15,32))])

def ranstring2():
    return ''.join([random.choice(ascii_letters) for i in range(random.randrange(3,7))])
    


inputfile = 'file.txt'

regmatch = '\'[^\'\r\n]+'
regvarmatch = '\$[a-zA-Z0-9\_]+'

finalout = []
stringdict = {}
finalstrings = []

#Get a random string for our new stringlist
stringvar = ranstring()

#Go through the inputfile one line at a time performing regex matching/replace.
with fileinput.FileInput(inputfile, inplace=False) as file:
    for line in file:
        
        #Find the String replacement in each line.
        fullmatch = re.findall(regmatch,line)
        #print(fullmatch)
        #For each match do the lookup and cleanup.        
        for f in fullmatch:
            #cleanup regex matches
            stripfull = f.replace("'",'')
            #split strings up and create a list
            stringlist = list(chunkstring(stripfull,5))
            #Add random data to stringlist
            ranlist = []
            for v in range(5):
               ranlist.append(ranstring2())
            #Keep a copy of the correct order.
            origstrings = stringlist.copy()
            #Wait to pad the list with random values until after the orig is copied
            stringlist.extend(ranlist)
            #mix it up
            random.shuffle(stringlist)

            pos = len(finalstrings)
            
            #Create a dict with new shuffled order,seeding with correct index value.
            stringdict = dict(enumerate(stringlist,start=pos))

            finalstrings.extend(stringlist)
            

            
            allkeys = []
            outkeys = ""
            for s in origstrings:
                for key,value in stringdict.items():

                    if(value == s):
                        allkeys.append(key)
                        newout = "+" + "$" + stringvar + "[" + str(key) + "]"
                        outkeys += newout
            
            line = line.replace(f,outkeys)
      
           
        #Add the new line for output
        line = line.replace("+","",1).replace("'","")
        finalout.append(line)


finalstringlist = str(finalstrings).replace("[","$"+stringvar+" = @(").replace("]",")")


#join our final list and find variables
listToStr = ' '.join([str(elem) for elem in finalout])
matchvars = re.findall(regvarmatch,listToStr)
#dedup regex list match
uniqvarlist = list(dict.fromkeys(matchvars))

#Strip out our previous randomly generated string array value
finalvarlist = []
for u in uniqvarlist:
    if (stringvar not in u):
        finalvarlist.append(u)

newstring = []
randToStringDict = {}

#Create a dict and map orig variable names to random
for final in finalvarlist:
    rep = ranstring()
    repstr = "$" + rep
    randToStringDict[final] = repstr

Invoke_string = "Invoke-WebRequest"
split_strings = []
n=2
count=0
split_vars = []
for index in range(0,len(Invoke_string),n):
    split_strings.append("$a"+str(count)+"='"+Invoke_string[index : index + n]+"'")
    split_vars.append("$a"+str(count))
    count += 1
splitvarsout = ''.join([str(elem1) for elem1 in split_vars])

#shuffle new split var list:
random.shuffle(split_strings)

updateval = ""
#Go through and perform replacement given the matched random string.   
for f in finalout:
    for final in finalvarlist:
        if Invoke_string in f:
            for s in split_strings:
                updateval += "\n"+s
            f = updateval + "\n" + "$c = " + '"' + f.replace(Invoke_string,splitvarsout) + '"' "\n" "IEX $c"
        if final in f:
            f = f.replace(final,randToStringDict[final])            
    newstring.append(f)




#Print out what we plan to write
print(finalstringlist)
for n in newstring:
    print(n)


outputfile = inputfile+".out"
print("Output file saved as: %s" % outputfile)
with open(outputfile, 'w') as f:
    f.write(finalstringlist)
    f.write("\n")
    for n in newstring:
        f.write(n)



