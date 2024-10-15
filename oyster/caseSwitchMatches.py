import re

def decodeIt(inputString, shift):
    result = ""
    tmp = inputString.split('[')
    for t in range(len(tmp)):
        result += chr(int(tmp[t])-shift)
    return result

test = """
Insert or read in code here

	"""


matches = re.findall('While\s[0-9]+[^\~]+', test, re.MULTILINE)

for m in matches:
    caseNum = re.findall('\$[a-zA-Z0-9]+\s\=\s[0-9]+',m)
    numValue = caseNum[0].split(' = ')[1]
    searchValue = f'Case {numValue}[^`]+'
    actual = re.findall(searchValue,m)
    test = test.replace(m,actual[0])


matchesDecode = re.findall('tuitiondelight[^\)]+',test)


for m in matchesDecode:
    temp = m.replace('tuitiondelight("','')
    temp = temp.split(',')
    try:
        decodedValue = decodeIt(temp[0].replace('"',''),eval(temp[1]))
    except:
        print(f'Skipped {temp}')
    test = test.replace(m+')',decodedValue)

with open("out.txt", "w") as file:
    file.writelines(test)
