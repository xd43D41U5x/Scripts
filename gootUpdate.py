import re

valDict = {}

def stMatch(cb):
    print('Starting search for all enc string variables...')
    rex = r'\w+\=\'.*?(?<!\\)\'\;'
    stringMatches = re.findall(rex,cb)
    for m in stringMatches:
        try:
            tmp = m.split("='",1)
            valDict[tmp[0]] = tmp[1][:-2]
        except:
            continue
    print(f'Finished search with {len(stringMatches)} items found...')
    print('Added to main lookup...')

def cMatch(cb):
    print('Starting search for items being joined or re-assigned...')
    catMatches = re.findall('\w+\s\=\s[\w\+\(\)]+',cb)
    for c in catMatches:
        #Handle items being joined together.
        try:
            if '+' in c:
                tmp = c.split(" = ")
                res = ''
                plusVals = tmp[1].split('+')
                for p in plusVals:
                    res = res + valDict[p]
                valDict[tmp[0]] = res
            else:
                #Handle items being set to other existing values.
                tmp = c.split(" = ")
                res = ''
                try:
                    tmpVal = valDict[tmp[1]]
                    valDict[tmp[0]] = tmpVal
                except:
                    continue
        except:
            continue
    print(f'Finished search with {len(catMatches)} items found...')
    print('Added to main lookup...')

def pMatch(cb):
    print('Starting search for main payload...')
    #Find the main/long payload for the next part.
    payMatch = re.findall('\w+\s*\=\s*[\w\+\(]{20,}\)',cb)
    res = ""
    for p in payMatch:
        p = p.split("(")
        tmp = p[1].replace('(','').replace(')','')
        yPlus = tmp.split('+')
        for y in yPlus:
            res = res + valDict[y]
    if payMatch:
        print('Payload found...')
    return res

def blockCheck(cb):
    bMatch = re.findall("\(\'([^\']{100,})\'\)",cb)
    return bMatch

def decode(encPay):
    print('Starting payload decode...')
    #Perform the decode/re-order based on string position.
    output = ''
    for index, char in enumerate(encPay):
        if(index % 2):
            output = output + char
        else:
            output = char + output
    return output

def getURLS(cb):
    #Find the url block
    urlBlock = ''.join(re.findall('htt.+\:\/\/[^\)]+',cb))
    #Find the short snippets of known values
    delim = ''.join(re.findall('htt[^\:]+',urlBlock))
    #Remove known values
    replacements = str.maketrans({"h": "", "t": "", "p": "", "s": "", ":" : "", "+" : ""})
    res = delim.translate(replacements)
    res = "".join(dict.fromkeys(res))
    #Remove the identified char and other known values.
    result = urlBlock.replace(res,"").replace('"','').replace('+','')
    result = result.split(",")
    print('URLs found: ')
    #Print results while defanging
    for r in result:
        r = r.replace('t','x').replace('.','[.]')
        print(r)


def prBanner(loopNum,output):
    print(f'************* Loop {loopNum} start - Lookup size = {len(valDict)} *****************')
    print(output)
    print(f'************* Loop {loopNum} end *****************')

def main():
    
    codeBlock = r"""Add diff code here"""
    loopCount = 1

    while (True):

        stMatch(codeBlock)
        cMatch(codeBlock)

        blCheck = blockCheck(codeBlock)
        if blCheck:
            print('Large single block found, decoding and looping again...')
            output = decode(blCheck[0].encode('utf-8').decode('unicode_escape'))
            prBanner(loopCount,output)
            codeBlock = output
            loopCount += 1
            if 'http' in codeBlock:
                print('Potential final block found, looking for URLs...')
                getURLS(codeBlock)
                break 
            continue

        result = pMatch(codeBlock)

        #Need to remove escape chars before doing the deob
        result = result.encode('utf-8').decode('unicode_escape')
        output = decode(result)

        prBanner(loopCount,output)
        codeBlock = output
        loopCount += 1

        if loopCount > 20 or codeBlock == '':
            print('Unexpected loop size encountered or code block empty, check initial values...')
        
        if 'http' in codeBlock:
                print('Potential final block found, looking for URLs...')
                getURLS(codeBlock)
                break
    
    

if __name__ == "__main__":
    main()
