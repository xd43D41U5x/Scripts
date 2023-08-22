repVals = ")zb)zbzbbzbz)bzb)bzb))zbbz)bzbbz))bzbzb)b))zb)bz)bzb))zbb))zb)bz"

char0 = repVals[0]
char1 = repVals[1]
char2 = repVals[2]

output = ""

for x in range(len(repVals)):
    if (repVals[x] == char0):
        output += "0"
    elif (repVals[x] == char1):
        output += "1"
    elif (repVals[x] == char2):
        output += "2"

print(output)
