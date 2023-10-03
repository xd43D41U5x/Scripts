import re
import os
import base64
import subprocess

def decodeB64(encVal,base64_dict):
  encBin = result = ""
  encVal = encVal.replace('=', '')

  #do lookups
  for i in encVal:
    keys = [k for k, v in base64_dict.items() if v == i] 
    keys_str = "".join(keys)
    encBin += keys_str 
  
  #break it into 8 bits, remove the 0 left
  encBin = [encBin[i:i+8] for i in range(0, len(encBin), 8)]
  if len(encBin[-1]) != 8:
    encBin.pop()
 
  #convert binary to ascii values, skip values we can't convert.
  #Could change continue to append if they are needed.
  for i in encBin:
    n = int(i, 2)
    try:
        result += n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass') or '\0'
    except:
        continue

  return result

#Leaving this function as it can be used to do encoding if needed in the future.
def encodeB64(a):
  l = []
  m = ""
  out = []
  for i in a:
    l.append(ord(i))
  for i in l:
    m += str(bin(i)[2:].zfill(8))
  for x in range(0,len(m),6):
    currentSet = m[x:x+6]
    if len(currentSet) < 6:
      currentSet = currentSet.ljust(6,'0')
    out.append(currentSet)

  return m

def configOut(resultName,listName,ver):
  print(f"Found possible config in list {ver}.")
  c2 = re.findall('http\:.+',resultName)
  listName.insert(0,c2[0]) 
  print("Config found: \n") 
  for c in listName:
    print(c)

def configCheck(convert1,convert2):
    print("Looking for the config in one result set...")
    check1 = re.findall('\d{1,2}\=.+',convert1)
    check2 = re.findall('\d{1,2}\=\.+',convert2)

    if len(check1) != 0:
        configOut(convert1,check1,1)
    elif len(check2) !=0:
        configOut(convert2,check2,2)
    else:
        print("No config found, review output...")

def writeResults(convert1,convert2):
    print("\nWriting out first result set as 'outputDecoded1.txt...'")
    with open("outputDecoded1.txt", "w") as f:
        f.write(convert1)

    print("Writing out second result set as 'outputDecoded2.txt...'")
    with open("outputDecoded2.txt", "w") as f:
        f.write(convert2)

def createTables(customTable):
    b64Table = {}
    for x in range(len(customTable)):
        b64Table[nums[x].zfill(6)] = customTable[x]
    return b64Table

def keyGen(key):
    #This is an area that could change, currently it appends an 'a'. Change here if needed.
    key = key.replace(key[0],'a',1)[:-1]
    updatedKey = len(key) ^ ord(key[0])
    for c in range(len(key)-1):
        updatedKey ^= ord(key[c+1])
    return updatedKey

def decryptString(payloadMatches):
    outBytes = bytearray()
    pay = bytes.fromhex(payloadMatches[2])
    pay = base64.b64decode(pay)
    for p in range(len(pay)):
        outBytes.append(~(pay[p] ^ updatedKey) & 0xFF)
    return outBytes

def genCmd(outFile):
    osType = os.name
    if osType == 'nt':
        cmd = "strings64 " + outFile
    else:
        cmd = "strings " + outFile
    return cmd

print("1. Provide raw binary file.")
print("2. Provide string output from final payload.")
option = input("Select Option: ")


#Leaving in as these were some test values used.
#encoded = "sxddWxsWAhuTmmiMxeZt7iXXpNdfsM1ESNdfWO1ESNdfWxdFsxzWAhgTO4qWAhCTO4qWAhpTWxzcWCdfEO1E SNdfsOzTgdKleIKAxeZFsO1ESNdfsOQTO4qWAhuM7iXXpNdfsOeTWzdfsO2ToyK2PI9cpkXPi0JUi0uWAhuI7 OeWAhu572cBxeZFEx1ESNdfsOlTO4qWAC"
#encoded = "iImYWLgHEItyESBHWw9rLSpC2wWhW4BO2SmwiINyESBHWw9rLSpC2wWhW4BO2SmwiINyESBHWw9rLSpC2wWh W4BO2SmwiINyESBHWw9rLSpC2wWhW4BO2SmwiINyESBHWw9rLSpC2wWhW4BO2SmwiINyESBHWw9r"
#encoded = "cU5kiYNoNUXV2wBY=UWCNIml=vcC=UN9N0M9QUZONLc9W0MC2nMYiUXV2wZJ=UoM2r9dWLp7=dc9fS+Y2Ja3=dchW0Mm2JXVWImoEwt9W0MeNU5kNvZA=UBANU9C2nMC2nMnNI93WUZkKA"

#Default string values that are exactly 64 chars in length and are the custom b64 tables here.
customTable1 = "zLAxuU0kQKf3sWE7ePRO2imyg9GSpVoYC6rhlX48ZHnvjJDBNFtMd1I5acwbqT+="
customTable2 = "aM0jd5Uv=gFu1pDKxcqeXZILEWi2fNQyVonOl9wr8hP73+HCAtkbY4SJRmsGTB6z"

#Bin numbers to create lookup dict
nums = "0,1,10,11,100,101,110,111,1000,1001,1010,1011,1100,1101,1110,1111,10000,10001,10010,10011,10100,10101,10110,10111,11000,11001,11010,11011,11100,11101,11110,11111,100000,100001,100010,100011,100100,100101,100110,100111,101000,101001,101010,101011,101100,101101,101110,101111,110000,110001,110010,110011,110100,110101,110110,110111,111000,111001,111010,111011,111100,111101,111110,111111"
nums = nums.split(',')

if option == '1':
    fileNameInput = input("File Name: ")
    print(f"Attempting to find payload and key in file {fileNameInput}...")
    
    with open(fileNameInput, "rb") as f:
        payloadOut = f.read()

    payloadHex = payloadOut.hex()
    #7c is the current known separator value.  Update here if that changes.
    if '7c' in payloadHex:
        payloadMatches = payloadHex.split('7c')
        key = bytearray.fromhex(payloadMatches[1]).decode()

        print(f"Raw key found of: {key}")
        updatedKey = keyGen(key)
        print(f"Fixed and final key calculated as: {hex(updatedKey)}")
        
        outBytes = decryptString(payloadMatches)
        outFile = fileNameInput + ".out"

        print(f"Writing out final payload as: {outFile}")
        with open(outFile,'wb') as f:
            f.write(outBytes)

        #check os for correct strings command, then run
        cmd = genCmd(outFile)
        stringsOutput = subprocess.check_output(cmd,shell=True)
        stringsFinal = stringsOutput.decode("utf-8")
        stringsFinal = stringsFinal.split('\n')

        #Look for exactly 64 char long string for possible custom tables
        regMatch = re.compile(r'^.{64}$')
        customTables = [s for s in stringsFinal if regMatch.match(s)]   

        if len(customTables) == 2:
            print(f"Possible tables found of {customTables}...\n")
            input("Should we use these or the default? (y/n)")
            if input == 'y':
                customTable1 = customTables[0]
                customTable2 = customTables[1]
            else:
                print("Custom tables not found, using default...")
                print("Creating custom B64 tables...")

        else:
           print("No table values found, proceeding to try default.")

        b64Table1 = createTables(customTable1)
        b64Table2 = createTables(customTable2)

        convert1 = convert2 = ""
        for s in stringsFinal:
            try:
                convert1 += decodeB64(s,b64Table1) + "\n"
                convert2 += decodeB64(s,b64Table2) + "\n"
            except:
                continue

        configCheck(convert1,convert2)
        writeResults(convert1,convert2)

    else:
       print("Default payload separator now found, review the file.")


elif option == '2':

    stringFile = input("File name containing strings output: ")

    print(f"Attempting to find possible custom b64 tables in string output file {stringFile}...")
    customTables = []
    with open(stringFile, "r") as f:
        for line in f:
            tableMatch = re.findall(r"^.{64}$",line)
            if len(tableMatch) != 0:
                customTables.append(tableMatch)

    if len(customTables) == 2:
        print(f"Possible tables found of {customTables}...\n")
        input("Should we use these or the default? (y/n)")
        if input == 'y':
            customTable1 = customTables[0]
            customTable2 = customTables[1]
    else:
       print("Custom tables not found, using default...")

    print("Creating custom B64 tables...")
    b64Table1 = createTables(customTable1)
    b64Table2 = createTables(customTable2)

    print("Reading in string file and attempting to convert all found strings for each table...")
    convert1 = convert2 = ""
    with open("allstring.txt", "r") as f:
        for line in f:
            try:
                convert1 += decodeB64(line,b64Table1) + "\n"
                convert2 += decodeB64(line,b64Table2) + "\n"
            except:
                continue
    
    configCheck(convert1,convert2)
    writeResults(convert1,convert2)
    

else:
    print("That wasn't valid input, run again and pick a number value.")
