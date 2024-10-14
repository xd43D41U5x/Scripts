using System.Runtime.InteropServices;
using System;
using System.IO;
using System.Runtime.CompilerServices;

const ushort COMPRESSION_FORMAT_LZNT1 = 2;

[DllImport("ntdll.dll")]
static extern uint RtlGetCompressionWorkSpaceSize(ushort CompressionFormat, out uint pNeededBufferSize, out uint Unknown);

[DllImport("ntdll.dll")]
static extern uint RtlDecompressFragment(ushort CompressionFormat, byte[] DestinationBuffer, int DestinationBufferLength, byte[] SourceBuffer,
    int SourceBufferLength, uint Unknown, out int pDestinationSize, IntPtr WorkspaceBuffer);

[DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
 static extern IntPtr LocalAlloc(int uFlags, IntPtr sizetdwBytes);

[DllImport("kernel32.dll", SetLastError = true)]
static extern IntPtr LocalFree(IntPtr hMem);


Console.WriteLine("Enter File to Decompress:");
string path = Console.ReadLine();
byte[] inputFile = File.ReadAllBytes(path);

var outBuf = new byte[inputFile.Length * 6];

uint dwSize = 0, dwRet = 0;
uint ret = RtlGetCompressionWorkSpaceSize(COMPRESSION_FORMAT_LZNT1, out dwSize, out dwRet);

int dstSize = 0;
IntPtr hWork = LocalAlloc(0, new IntPtr(dwSize));
ret = RtlDecompressFragment(COMPRESSION_FORMAT_LZNT1, outBuf,
   outBuf.Length, inputFile, inputFile.Length, 0, out dstSize, hWork);
LocalFree(hWork);

string outPath = path + ".out";
File.WriteAllBytes(outPath, outBuf);
