#Api hash lookup for Ghidara using json output file.
#@author d43D41U5
#@category Analysis
#@keybinding 
#@menupath 
#@toolbar 

import json
import csv

hash_path = askFile("Json Output", "Choose file:")
hash_path = str(hash_path)
data = ""

#Read in CSV data and parse to Dict
with open(hash_path, "r") as file:
	data = csv.DictReader(file)
    	dataDict = {row['Hash']: row for row in data}

#Api Function call - update to match unique sample
api_fn_addr = toAddr(0x000003cc)
fn_refs = getReferencesTo(api_fn_addr)

output = ''

for ref in fn_refs:
	from_addr = ref.getFromAddress()
	tmp = getInstructionBefore(from_addr)
	instr = getInstructionBefore(tmp)
	hash = instr.getOpObjects(1)[0].toString()

	
	
	if '0x' in hash:
		hashVal = dataDict.get(hash,'NotFound')
		if (hashVal != 'NotFound'):
			print(from_addr.toString() + ' : ' + hash + ' : ' + hashVal['Function'])
			setPreComment(from_addr, hashVal['Function'])
			createBookmark(from_addr, 'ApiHash', hashVal['Function'])
			output += from_addr.toString() + ',' + hash + ',' + hashVal['Function'] + '\n'

out_path = askFile("Output File", "Choose file:")
out_path = str(out_path)
with open(out_path, "w") as file:
	file.write(output)
