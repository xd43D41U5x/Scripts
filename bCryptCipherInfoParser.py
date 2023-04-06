#This script will parse BCRYPT_AUTHENTICATED_CIPHER_MODE_INFO from BCrypt.
#Was written for AES GCM for the 3CX analyisis.
#This structure will be seen as the padding info param on the call to BCrypt.
#Documented structure here: https://learn.microsoft.com/en-us/windows/win32/api/bcrypt/ns-bcrypt-bcrypt_authenticated_cipher_mode_info
#Note: the pb blocks will not be the actual value but a ptr to a memory location with the needed data in the size in cb.

def littleEn(pMessage,data):
    temp = []
    for i in range(0, len(data), 2):
        temp.append(data[i:i+2])
    out = (''.join(temp[::-1])).lstrip('0')
    if (out == ''):
        out = '0'
    print(f'{pMessage}: 0x{out}')

cipherModeInfoBlock = "5800000001000000E0E27F82610000000C0000000000000000000000000000000000000000000000446FC42EFB010000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

blockStruct = {"cbSize":"0-8","dwInfoVersion":"8-16","pbNonce ":"16-32",
               "cbNonce":"32-40","pbAuthData":"40-56","cbAuthData":"56-64",
               "pbTag":"80-96","cbTag":"96-104","pbMacContext":"112-128",
               "cbMacContext":"128-136","cbAAD":"136-144","cbData":"144-160",
               "dwFlags":"160-168"
               }

for k,v in blockStruct.items():
     b = v.split('-')
     littleEn(k,cipherModeInfoBlock[int(b[0]):int(b[1])])
