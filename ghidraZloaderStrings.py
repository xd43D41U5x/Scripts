#TODO write a description for this script
#@author d43D41U5
#@category Analysis
#@keybinding 
#@menupath 
#@toolbar 

from ghidra.app.decompiler import DecompileOptions
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.program.model.listing import FunctionSignature
func_manager=currentProgram.getFunctionManager()
func_iterator=func_manager.getFunctions(True)
from ghidra.program.model.pcode import FunctionPrototype
import re
import json
import codecs


def xor(data):
	key = '3C33BC546F511439A4B56252799876FBB0'
	key = bytearray.fromhex(key)
	l = len(key)
	return(bytearray(((data[i] ^ key[i % l]) for i in range(0,len(data)))))

def get_high_function_c(func):
	options = DecompileOptions()
	ifc = DecompInterface()
	ifc.setOptions(options)
	ifc.openProgram(getCurrentProgram())
	res = ifc.decompileFunction(func, 60, monitor)
	funC = res.getDecompiledFunction().getC()
	high_func = res.getHighFunction()
	lsm = high_func.getLocalSymbolMap()
	symbols = lsm.getSymbols()
	return funC,symbols

def getCallingFunList(addy):
	api_fn_addr = toAddr(addy)
	fn_refs = getReferencesTo(api_fn_addr)
	callList = []
	for ref in fn_refs:
		from_addr = ref.getFromAddress()
		callingFunName = getFunctionContaining(from_addr)
		if callingFunName != None:
			callingFunName = callingFunName.toString()
			if callingFunName not in callList:
				callList.append(callingFunName)
	return callList


def setBC(addy, plainStringsDict):
	api_fn_addr = toAddr(addy)
	fn_refs = getReferencesTo(api_fn_addr)
	for ref in fn_refs:
		from_addr = ref.getFromAddress()
		instr = getInstructionBefore(from_addr)
		prevInstr = getInstructionBefore(instr)
		datRef = prevInstr.getOpObjects(1)[0]
		datRef = datRef.toString().replace('0x','')
		for key, value in plainStringsDict.iteritems():
			if key == datRef:
				setPreComment(from_addr, 'String Deob: ' + value)
				createBookmark(from_addr, 'DecodedStrings', value)

def decryptStrings(callList):
	xorDict = {}
	xorResultDict = {}
	for func in func_iterator:
    		if func.getName() in callList:
			hfC, symbols = get_high_function_c(func)
			xorFun = re.findall('FUN_2116a82ae10[^\;]+',hfC)
			for x in xorFun:
				xorTemp = x.split('&',1)
				xorTemp = xorTemp[1].split(',')
				xorDat = xorTemp[0].replace('DAT_','')
				xorVar = xorTemp[1].replace('(longlong)','').replace(')','').strip()
				xorDict[xorDat] = xorVar
			for i, symbol in enumerate(symbols):
				for key, value in xorDict.iteritems():
					if value == symbol.getName():
						plainBytes = getBytes(toAddr(key),symbol.size)
						xorResult = xor(bytearray(plainBytes))
						try:
							xorResultDict[key] = xorResult.decode().replace('\x00','')
						except:
							xorResultDict[key] = codecs.getencoder('hex')(xorResult)[0]
	return xorResultDict


#Update this address to match the correct xor function
funAddy = '0x2116a82ae10'
callingList = getCallingFunList(funAddy)
xorResultsDict = decryptStrings(callingList)
setBC(funAddy,xorResultsDict)


out_path = askFile("Output File", "Choose file:")
out_path = str(out_path)
with open(out_path, "w") as file:
	file.write(json.dumps(xorResultsDict))
				      
