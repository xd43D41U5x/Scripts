**The Frida Script here is to automatically dump the second stage payload for BumbleBee malware**

**Usage**  
_python BumbleBeeDump.py "C:\Windows\System32\rundll32.exe" C:\Users\IEUser\Desktop\file\file.dll,SetPath"_


**This script/review/research was completely based on the excellent write-up here:**  
https://elis531989.medium.com/the-chronicles-of-bumblebee-the-hook-the-bee-and-the-trickbot-connection-686379311056

**OverView**  
So, the normal process of setting breakpoints on things like VirtualAlloc and VirtualProtect to dump the second stage payload do not work well or as expected in this case.  This loader/unpacker is specifially using those for hooking NTdll functions related to LoadLibrary.  If we try to set breakpoint on those or even LoadLibrary, what we will end up with is the payload but a memory mapped version of it.  That doesn't really help here and we would like what is seen on disk to perform further analysis with things like Ghidra.

**Initial Thoughts**  
Ok, fine I can't break on the normal items, then where can I break if I don't have time to reverse the entire thing statically such as was done in the write-up listed.  There are loops in specific functions that are writing out the unpacked code but those are just typical loops and it doesn't appear to be using something like memcpy (or other similar items for the move).

**Where to catch it**  
Our best bet is to try and catch the reservation of the memory region where this will be written and monitor that for an executable.  This malware appears to be using HeapAlloc to perform these operations.  However, the problem with HeapAlloc is it can be called hundreds of times as this is commonly used for small memory operations.  It's very difficult to set a breakpoint and step through that many times, then monitor the region reserved in hopes it writes there.

**The Solution**  
The easiest way is to script this and let it do the work for us.  We know we want to monitor HeapAlloc and we know that it will be a sizable memory reservation.  The HeapAlloc function takes size on entry as the 3rd parameter, then has a return value of a pointer to the allocated block of memory.  So lets have our script go through each onEnter value when HeapAlloc is called, check the size and if its not large (ie: program size), ignore it.  However, if its a good size, lets save that memory location that is returned along with the size and watch those for signs of an MZ header (4d 5a 90 00).
We can use Frida for this as it can hook the program and intercept the calls for HeapAlloc, then monitor our onEnter and onLeave values.  Once we find an item of interest, dump that exact memory region using the base address returned from the function call along with the size passed in.

**Example Output**  
```
HeapAlloc called => Size: 0x26f014
HeapAlloc returned => Address: 0x2396f69e040

HeapAlloc called => Size: 0x40d36c
HeapAlloc returned => Address: 0x2396fab1040

HeapAlloc called => Size: 0x40d36c
HeapAlloc returned => Address: 0x2396fec2040

HeapAlloc called => Size: 0x243200
HeapAlloc returned => Address: 0x239702ec040

HeapAlloc called => Size: 0x243200
HeapAlloc returned => Address: 0x23970549040

Memory.scan() found match at 0x23970549040 with size 4
Dumped file: dump_mz116.bin
```

