def subCipher(encoded): 
   out = [] 
   for e in encoded: 
       if e in cipherAlphabet: 
           out.append(decodedAlphabet[cipherAlphabet.find(e)]) 
       else: 
           out.append(e) 
   return "".join(out)

decodedAlphabet = ";AeDR6My.8B>N^-[<pG:kbKFQmHwS1lt&sc=/_vi}2a$9X,)gWhVUf?Lq7P0(!+oI4 u{rJCn]ZxOY*3E5dzTj"
cipherAlphabet = "2w !8dnUDqA.sy*ILCkl?E5/>a+gRG)P-VNSF(BtfX^mo&${_]:4MjW;61QHxKb[r=vYzu3hpO9<ZcJi07T}e,"

enc = "AYt)PrpDAtp^uUDk}tC! N[aCu VV"


print(subCipher(enc))
