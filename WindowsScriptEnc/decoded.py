def decode(s):
    t = ""
    for i in range(len(s)):
        ascii = ord(s[i])
        c = chr(ascii)
        if (ascii == 42):
            c = chr(92)
        elif (ascii == 36):
            c = chr(47)
        elif (ascii == 126):
            c = chr(58)
        elif (ascii == 124):
            c = chr(46)
        elif (ascii == 33):
            c = chr(37)
        elif (ascii == 35):
            c = chr(38)
        elif (ascii == 61):
            c = chr(95)
        elif (65 <= ascii & ascii <= 90):
            c = chr((ascii - 65 + 15) % 26 + 65)
        elif (97 <= ascii & ascii <= 122):
            c = chr((ascii - 97 + 15) % 26 + 97)
        t += c
    return t

print(decode("nxo $n azhpcdspww thc -zfeq !exa!*lwr|pip seead~$$wlmtxj|tyv$cdvxp # delce !exa!*lwr|pip"))
