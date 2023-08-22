output = ""
output += chr(9)*64
for x in range(32,127,1):
    output += (chr(x)*64)

print(output)
