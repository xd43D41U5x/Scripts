#Easy/Quick way to use one file as a known good source and then
#check a suspected malicious file line by line, searching the legit file for hits.
#Anything that isn't found is saved to a new file for review.
#This is better than a line vs line comparision as there are too many ways that could be off.
#This was specifically written for the new versions of gootloader but could be used with anything.

import fileinput

#read in legit code
with open('legit.txt','r') as legitFile:
        fulllegitFile = legitFile.read()
    
#go through malicious code line/line then search legit
result = []
with fileinput.FileInput('malfile.txt', inplace=False) as file:
    for line in file:
        if line not in fulllegitFile:
            result.append(line)

#Save results
with open('output.txt','w') as outputFile:
    for r in result:
            outputFile.write(r)

print(f'File written with {len(result)} total found result lines.')
