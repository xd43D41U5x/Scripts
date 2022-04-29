from numpy import base_repr
import base64
import re

#nbrut is the obfuscated code
nbrut = ""
utnbr = ""
nbr = ""
yun = []
#test is the string list
test = ""

ut = test.split("|")



def uyn(charcode,utnbr):
    if (charcode < utnbr):
        out = ""
    else:
        out = str(int(charcode/utnbr))
                  
    if ((charcode % utnbr) > 35):
        charcode = charcode % utnbr
        out += chr(charcode + 29)
    else:
        charcode = charcode % utnbr
        out += base_repr(charcode,36).lower()

    return out
    

def replace_substrings(s, d):
    p = "|".join(d.keys())
    p = r"(?<!\w)(" + p + r")(?!\w)"
    return re.compile(p).sub(lambda m: d[m.group(0)], s)

valuedict = dict()

for x in range(nbr-1,-1,-1):
    place = uyn(x,utnbr)
    if (ut[x] == ""):
        item = place
    else:
        item = ut[x]
    valuedict[place] = item
    
print(repr(replace_substrings(nbrut, valuedict)))
