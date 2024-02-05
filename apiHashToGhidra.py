#The original script was pulled from https://blog.nviso.eu/2021/09/02/anatomy-and-disruption-of-metasploit-shellcode/
#It has been modified since to support a unique hashing variation as well as writing the output to json to support ghidra scripting for lookups.

import glob
import os
import pefile
import sys
import json
 
size = 32
mask = ((2**size) - 1)
 
# Resolve 32- and 64-bit System32 paths
root = os.environ.get('SystemRoot')
if not root:
    raise Exception('Missing "SystemRoot" environment variable')
 
globs = [f"{root}\\System32\\*.dll", f"{root}\\SysWOW64\\*.dll"]
 
# Helper function for rotate-right
def ror(number, bits):
    return ((number >> (bits % size)) | (number << (size - (bits % size)))) &  mask
 
# Define hashing algorithm
def api_hash(name):
    out = 0
    name = upper(name)
    for n in name:

        out = (out << 4) + (n + 1)

        if out & 0xf0000000 != 0:
            fun1 = out & 0xD8A0FD01
            temp = (out & 0xf0000000) >> 0x18
            out = (out ^ 0xffffffff) & 0x275F02FE
            fun2 = (0xFFFFFFFF ^ temp) & 0x275f02fe
            after_fun2 = 0xD8A0FD01 & temp
            fun3 = out | fun1
            out = ((after_fun2 | fun2) ^ fun3) & 0xfffffff

    return hex(out ^ 0x5EE05984)
 
# Helper function to uppercase data
def upper(data):
    return [(b if b < ord('a') else b - 0x20) for b in data]
 
# Print CSV header
print("File,Function,Hash")
out = {}
# Loop through all DLLs
for g in globs:
    for file in glob.glob(g):
        # Compute the DllHash
        name = upper(os.path.basename(file).encode('UTF-16-LE') + b'\x00\x00')
        #file_hash = get_hash(name)
        try:
            # Parse the DLL for exports
            pe = pefile.PE(file, fast_load=True)
            pe.parse_data_directories(directories = [pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]])
            if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
                # Loop through exports
                for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                    if exp.name:
                        # Compute ExportHash
                        name = exp.name.decode('UTF-8')
                        exp_hash = api_hash(exp.name)
                        
                        # Print CSV entry
                        #print(f"\"{file}\",\"{name}\",\"{exp_hash}\"")

                        #Create dict with output values for Ghidara
                        out[str(exp_hash)] = name
        except pefile.PEFormatError:
            print(f"Unable to parse {file} as a valid PE, skipping.", file=sys.stderr)
            continue

with open('jsonOut.txt', 'w') as fileOut:
    fileOut.write(json.dumps(out))
