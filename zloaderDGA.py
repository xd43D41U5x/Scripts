import datetime

def getMidToday():
    now = datetime.datetime.now(datetime.timezone.utc)
    midnight = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    timeStampToday = midnight.timestamp()
    return timeStampToday


time = int(getMidToday())

results = []
for x in range(0x20):
    letters = ''
    for x in range(0x14):
        timeMain = hex(int(time / 0x19))
        currChar = int((time % 0x19)) + 0x61
        timeMain = str(timeMain)[:-2] + str(hex(currChar)).replace('0x','')
        letters += chr(currChar)
        shL = ((int(time) + currChar)<<0x8)&0xffffffff
        shR = ((int(time) + currChar)>>0x18)&0xFF
        time = shL | shR
    results.append(letters + '.com')

for r in results:
    print(r)
