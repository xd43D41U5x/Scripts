key = "9626189327398744517410513847136652"

#Create Zero'd list in the correct size.
resultData = [0] * 0x100

#Populate list with counts
for x in range(0x100):
    resultData[x] = x

temp = 0
for y in range(0,len(resultData),len(key)):
    hexResult = []
    for z in range(0,len(key)):
        rangePOS = resultData[y]
        keyPOS = ord(key[z])
        temp = (rangePOS + keyPOS + temp) & 0xFF
        resultData[y] = resultData[temp]
        resultData[temp] = rangePOS
        if y < len(resultData)-1:
            y+=1
        else:
            break
    for v in range(len(resultData)):
        hexResult.append("{:02x}".format(resultData[v]))
        
startPad = ["{:02}".format("00")]*8
endPad = ["{:02}".format("00")]*9

hexResult2 = startPad + hexResult + endPad
finalReuslt = " ".join(hexResult2)

#####Round two#######

count = 0
firstRes = 0
largeDataPos = 0
prevResult = 0
defTheFinal = []

with open('hexOutPlain.txt', 'r') as file:
    largeBinData = file.read()

largeBinData = largeBinData.split(" ")

for x in range(len(largeBinData)):

    count = (count + 1) & 0xFF
    orig = resultData[count]
    curDecodeChar = (orig + firstRes) & 0xFF
    firstRes = curDecodeChar
    temp2 = resultData[curDecodeChar]
    xorSetup = (resultData[count] + temp2) & 0xFF
    resultData[count] = temp2
    resultData[curDecodeChar] = orig
    xorSetup = resultData[xorSetup]
    largeBinData[x] = int(largeBinData[x],16) ^ xorSetup

for v in range(len(largeBinData)):
        defTheFinal.append("{:02x}".format(largeBinData[v]))

defTheFinalResult = " ".join(defTheFinal)

with open('results.txt', 'w') as f:
    f.write(defTheFinalResult)
