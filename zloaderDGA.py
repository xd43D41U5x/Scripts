import datetime

def getMidToday():
    now = datetime.datetime.now(datetime.timezone.utc)
    midnight = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    timeStampToday = int(midnight.timestamp())
    return timeStampToday

time = getMidToday()

results = []
for x in range(0x20):
    letters = ''
    for x in range(0x14):
        currChar = (time % 0x19) + 0x61
        letters += chr(currChar)
        time = (((time + currChar)<<0x8)&0xffffffff) | (((time + currChar)>>0x18)&0xff)
    results.append(letters + '.com')

for r in results:
    print(r)
