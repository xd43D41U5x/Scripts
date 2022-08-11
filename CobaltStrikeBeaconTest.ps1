#Usage ./CobaltStrikeBeaconTest.ps1 <file> <writefile>(optional)
param (
        [Parameter(Mandatory = $True)]
		[string]$Path,
        [Parameter(Mandatory=$false)]
        [ValidateSet(”writefile”)]
        [string] $writefile
	)  

if ($Path -eq "h")
{
    Write-Host "Usage"
    Write-Host "./beacontest.ps1 <file> <writefile>(optional)"
    Write-Host "Example"
    Write-Host "./beacontest.ps1 C:\Users\REM\Desktop\cbbeacon.exe writefile"
    exit
}

function xorbytes
{
    Param(
        [Parameter(Mandatory = $True)]
        [Byte[]]  $bytes,
        [Parameter(Mandatory = $True)]
        $key)
    for($i=0; $i -lt $bytes.count ; $i++)
    {
    $bytes[$i] = $bytes[$i] -bxor $key
    }
    if ($writefile -ne "")
    {
        #write file out in bytes
        [System.IO.File]::WriteAllBytes("$oFile", $bytes)
        write-host "[!] " -foregroundcolor green -nonewline; Write-host "File: " -nonewline; Write-host "$Path " -foregroundcolor yellow -nonewline;Write-host "XOR'd with key " -nonewline;Write-host "$key. " -foregroundcolor cyan -nonewline;Write-host "Saved to " -nonewline;Write-host "$oFile" -foregroundcolor yellow -nonewline;Write-host ".";
    }
    exit
}

#function to help parse pe file header    
function Local:Morph-Int{
    Param(
        [Parameter(Position = 1, Mandatory = $True)]
        [Byte[]]
        $array)
    switch ($array.Length){
        # Convert to WORD & DWORD
        2 { Write-Output ( [UInt16] ('0x{0}' -f (($array | % {$_.ToString('X2')}) -join '')) ) }
        4 { Write-Output (  [Int32] ('0x{0}' -f (($array | % {$_.ToString('X2')}) -join '')) ) }
    }
}
    
function patternmatch
{
    Param(
        [Parameter(Mandatory = $True)]
        [String[]] $hexpattern,
        [Parameter(Mandatory = $True)]
        [Byte[]]  $bytevalue)
    
    if ($hexpattern -match ‘2e-2f-2e-2f-2e-2c.{7}2e-2c-2e-2f-2e-2c.{7}2e’)
    {
        Write-Host "Confirmed this is a non-encrypted Cobalt Strike Beacon v4"
        xorbytes $bytevalue "0x2e"
    }
    elseif ($hexpattern -match ‘69-68-69-68-69-6b.{7}69-6b-69-68-69-6b.{7}69-6a’)
    {
        Write-Host "Confirmed this is a non-encrypted Cobalt Strike Beacon v3"
        xorbytes $bytevalue "0x69"
    }
    else
    {
        Write-Host "This does not appear to be a beacon."
    }
}

# Read File bytes
$bytes = [System.IO.File]::ReadAllBytes($Path)

#Set output file
$oFile = $Path + ".out"

#Convert bytes to hex for known pattern matching. 
$tohex = [System.BitConverter]::ToString($bytes)

#check to see if its a possible match as is.
patternmatch $tohex $bytes

Echo "Checking for possible encryption."
Echo "Attempting find the xor key and decrypt."
    
# Use PE offset for calculations
$PE = Morph-Int $bytes[63..60]
# Number of PE sections
$NumOfPESection = Morph-Int $bytes[($PE+7)..($PE+6)]
# Optional Header Size
$OptSize = Morph-Int $bytes[($PE+21)..($PE+20)]
# Use Optional Header start for calculations
$Opt = $PE + 24 
# Sections Table offset for calculations
$SecTbl = $Opt + $OptSize
    
# Loop through PE Sections based on $NumOfPESection
$SecOff = 0
$datasection = "False"
for($i=0; $i -lt $NumOfPESection; $i++){
    $SecName = [System.Text.Encoding]::ASCII.GetString($bytes, ($SecTbl+$SecOff), 8)
    if ($SecName -eq ".data")
    {
        $SecVirtualSize = Morph-Int $bytes[($SecTbl+$SecOff+11)..($SecTbl+$SecOff+8)]
        $SecVirtualAddress = '{0:X8}' -f (Morph-Int $bytes[($SecTbl+$SecOff+15)..($SecTbl+$SecOff+12)])
        $SecRawData = Morph-Int $bytes[($SecTbl+$SecOff+19)..($SecTbl+$SecOff+16)]
        $SecPTRRawData = '{0:X8}' -f (Morph-Int $bytes[($SecTbl+$SecOff+23)..($SecTbl+$SecOff+20)])
        $SectionFlag = '{0:X8}' -f (Morph-Int $bytes[($SecTbl+$SecOff+39)..($SecTbl+$SecOff+36)])
        $lengthofdata = [System.Convert]::ToString($SecRawData,16)
        $SecPTRRawData1 = (Morph-Int $bytes[($SecTbl+$SecOff+23)..($SecTbl+$SecOff+20)])
        $SecPTRRawData2 = '{0:X}' -f (Morph-Int $bytes[($SecTbl+$SecOff+23)..($SecTbl+$SecOff+20)])
        
        #write-host "data length: $lengthofdata"
        #write-host "start offset: $SecPTRRawData1"
        $endoffset = [int]$SecPTRRawData2 + [int]$lengthofdata
        #write-host "End offset: $endoffset"
        Echo "Found .Data Section in PE header!"
        Echo "Start offset at: 0x$SecPTRRawData"

        # Print Results - keeping if needed in future for debug
        #Echo "Section Name:    $SecName"
        #Echo "Virtual Size:    $SecVirtualSize bytes"
        #Echo "Virtual Address: 0x$SecVirtualAddress"
        #Echo "Raw Data Size:   $SecRawData bytes"
        #Echo "Raw Data PTR:    0x$SecPTRRawData"
        

        #Set flag to indicate a valid data section was found.
        $datasection = "True"
    }
    
    # Adjust $SecOff + 40 (0x28)
    $SecOff = $SecOff + 40
}

if ($datasection -ne "True")
{
    Echo "Was not able to identify a .data section, exiting"
    exit
} 

#Take identified .data section and strip that from the entire file for use.   
$intstart=[Int32]"0x$SecPTRRawData2"
$intend=[Int32]"0x+$endoffset"
$stripdatasection = $bytes[$intstart..$intend]
$hexdata = [System.BitConverter]::ToString($stripdatasection)

    
#Go through the entire .data section 4 bytes at a time, then use those looking for patterns indicating a repeating xor key.
$zerovalue = "00-00-00-00"
$offset = 0
$xorkeyfound = "False"
while ($offset -lt $stripdatasection.length)
{
    $key = $stripdatasection[$offset..($offset+3)]
    $hexkey = [System.BitConverter]::ToString($key)
    if ($hexkey -ne $zerovalue){
        
    $Matches = Select-String -InputObject $hexdata -Pattern "$hexkey" -AllMatches

    if ($Matches.Matches.Count -ge 1100)
    {
        Echo "Xor key found!"
        Echo $hexkey
        $xorkeyfound = "True"
        break
    }
    }
        
    $offset += 4
}

if ($xorkeyfound -ne "True")
{
    Echo "No key could be found, exiting"
    exit
}    
 

#Take hexkey and split into bytes for xor usage.
$keyarray = $hexkey -split "-"
    
#xor with rotating 4 byte key
for($i=0; $i -lt $stripdatasection.count ; $i++)
{
    $keyround = "0x"+$keyarray[$i % 4]
    $stripdatasection[$i] = $stripdatasection[$i] -bxor $keyround
}

$oFile2 = $Path + ".decode"

#Write decrypted bytes out to file - debug only.
#[System.IO.File]::WriteAllBytes("$ofile2", $stripdatasection)

Echo "Decrypt Complete, checking for known beacon patterns"

#Convert bytes to hex for pattern matching.
$tohex2 = [System.BitConverter]::ToString($stripdatasection)

#Attempt to pattern match again now that its decrypted.
patternmatch $tohex2 $stripdatasection
