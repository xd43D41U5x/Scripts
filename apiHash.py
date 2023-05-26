#This script was pulled from https://blog.nviso.eu/2021/09/02/anatomy-and-disruption-of-metasploit-shellcode/

import glob
import os
import pefile
import sys
 
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
def get_hash(data):
    result = 0
    for b in data:
        result = ror(result, 0x0D)
        result = (result + b) & mask
    return result
 
# Helper function to uppercase data
def upper(data):
    return [(b if b < ord('a') else b - 0x20) for b in data]
 
# Print CSV header
print("File,Function,Hash")
 
# Loop through all DLLs
for g in globs:
    for file in glob.glob(g):
        # Compute the DllHash
        name = upper(os.path.basename(file).encode('UTF-16-LE') + b'\x00\x00')
        file_hash = get_hash(name)
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
                        exp_hash = get_hash(exp.name + b'\x00')
                        metasploit_hash = (file_hash + exp_hash) & 0xffffffff
                        
                        # Print CSV entry
                        print(f"\"{file}\",\"{name}\",\"{hex(metasploit_hash)}\"")
        except pefile.PEFormatError:
            print(f"Unable to parse {file} as a valid PE, skipping.", file=sys.stderr)
            continue
