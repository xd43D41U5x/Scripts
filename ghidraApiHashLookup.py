#Api hash lookup for Ghidara using json output file.
#@author d43D41U5
#@category Analysis
#@keybinding 
#@menupath 
#@toolbar 

import json

hash_path = askFile("Json Output", "Choose file:")
hash_path = str(hash_path)
data = ""
with open(hash_path, "rb") as file:
	data = file.read()
	data = json.loads(data)

#Api Function call - update to match unique sample
api_fn_addr = toAddr(0x2116a82bd60)
fn_refs = getReferencesTo(api_fn_addr)

output = ''

for ref in fn_refs:
	from_addr = ref.getFromAddress()
	instr = getInstructionBefore(from_addr)
	hash = instr.getOpObjects(1)[0].toString()
	
	if '0x' in hash:
		hashVal = data.get(hash,'NotFound')
		if (hashVal != 'NotFound'):
			print(from_addr.toString() + ' : ' + hash + ' : ' + hashVal)
			setPreComment(from_addr, hashVal)
			createBookmark(from_addr, 'ApiHash', hashVal)
			output += from_addr.toString() + ',' + hash + ',' + hashVal + '\n'

out_path = askFile("Output File", "Choose file:")
out_path = str(out_path)
with open(out_path, "w") as file:
	file.write(output)
