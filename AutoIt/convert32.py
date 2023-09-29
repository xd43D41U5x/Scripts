fileName = input("Enter possible script file: ")

print("Reading in AutoItSC.bin Stub\n")
with open("AutoItSC.bin", "rb") as file:
    stubFile = file.read()

print("Reading in Script File\n")
with open(fileName, "rb") as file:
    scriptFile = file.read()

print("Attempting to find start of AutoIt Script...")

if b"\xA3\x48\x4B\xBE\x98\x6C\x4A\xA9\x99\x4C\x53\x0A\x86\xD6\x48\x7D" in scriptFile:
    scriptHit = scriptFile.find(b"\xA3\x48\x4B\xBE\x98\x6C\x4A\xA9\x99\x4C\x53\x0A\x86\xD6\x48\x7D")

    print(f"Script file found at offset {hex(scriptHit)}\n")
    
    with open(fileName + ".a32.exe", "wb") as file:
        file.write(stubFile + scriptFile[scriptHit:])

    print(f"Created 32bit version with name: {fileName}.a32.exe\n")
else:
    print("Script not found")
