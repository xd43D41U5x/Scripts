#Easy way to decode found SocGholish initial strings.  These are normally found on the compromised initial site or in the first few scripts returned.
import re
encodedFun = """Encoded Data"""

def strdecode(instr):
    output = ""
    for x in range(len(instr)):
        if(x%2):
            output += instr[x]
    return output

#find decode function name
fname = re.findall(r'\w{2}\(\'',encodedFun)
decodefun = (max(fname,key=fname.count)).replace("('","")
print(f'Found decode function with name: {decodefun}\n')
print(f'Starting Decode...\n')

regex = decodefun+'\(\'([^\']+)'
finding = re.findall(regex,encodedFun)

for f in finding:
    encodedFun = encodedFun.replace(f,strdecode(f))

#clean function name
encodedFun = encodedFun.replace(decodefun,'')
print(encodedFun)
