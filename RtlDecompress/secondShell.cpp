#include <Windows.h>
#include <stdio.h>
#include <string>
#include <iostream>

int main()
{
	int ret = 0;
	int err = 0;
	DWORD shellSize = 0;
	std::string shellName;
	char anotherFile;
	char hold;
	SIZE_T sizeEmpty = 272;
	std::string paramFile;
	std::string paramFile2;
	DWORD encSize = 0;
	DWORD encSize2 = 0;

	printf("What is the name of the Shellcode file? ");
	std::cin >> shellName;

	printf("What is the name of the param file? ");
	std::cin >> paramFile;

	printf("What is the name of the 2nd param file? ");
	std::cin >> paramFile2;

	printf("[+] Opening Shellcode File: %s\n", shellName.c_str());
	printf("[+] Opening Ecrypted File: %s\n", paramFile.c_str());
	printf("[+] Opening Final File: %s\n", paramFile2.c_str());

	HANDLE shellFile = CreateFileA(shellName.c_str(), GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	HANDLE encFile = CreateFileA(paramFile.c_str(), GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	HANDLE encFile2 = CreateFileA(paramFile2.c_str(), GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);

	if (shellFile == INVALID_HANDLE_VALUE)
	{
		err = GetLastError();
		printf("[-] ERROR: Unable to open Shell file. Error %i\n", err);
		return 0;
	}
	if (encFile == INVALID_HANDLE_VALUE)
	{
		err = GetLastError();
		printf("[-] ERROR: Unable to open Param file. Error %i\n", err);
		return 0;
	}
	if (encFile2 == INVALID_HANDLE_VALUE)
	{
		err = GetLastError();
		printf("[-] ERROR: Unable to open Final file. Error %i\n", err);
		return 0;
	}

	shellSize = GetFileSize(shellFile, NULL);
	encSize = GetFileSize(encFile, NULL);
	encSize2 = GetFileSize(encFile2, NULL);

	if (shellSize == INVALID_FILE_SIZE)
	{
		err = GetLastError();
		printf("[-] ERROR: Shell file GetFileSize error %i\n", err);
		CloseHandle(shellFile);
		return 0;
	}
	if (encSize == INVALID_FILE_SIZE)
	{
		err = GetLastError();
		printf("[-] ERROR: Param File GetFileSize error %i\n", err);
		CloseHandle(encFile);
		return 0;
	}
	if (encSize2 == INVALID_FILE_SIZE)
	{
		err = GetLastError();
		printf("[-] ERROR: Param File GetFileSize error %i\n", err);
		CloseHandle(encFile2);
		return 0;
	}

	printf("[+] Shell File Size: %i bytes\n", shellSize);
	printf("[+] Param File Size: %i bytes\n", encSize);
	printf("[+] Param File Size: %i bytes\n", encSize2);
	printf("[+] Allocating memory buffer...\n");

	void* pShellcode = VirtualAlloc(NULL, shellSize, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	void* pEncCode = VirtualAlloc(NULL, encSize, MEM_COMMIT, PAGE_READWRITE);
	void* pEncCode2 = VirtualAlloc(NULL, encSize2, MEM_COMMIT, PAGE_READWRITE);

	if (pShellcode == NULL)
	{
		err = GetLastError();
		printf("[-] ERROR: Shell File VirtualAlloc error %i\n", err);
		CloseHandle(shellFile);
		return 0;
	}
	if (pEncCode == NULL)
	{
		err = GetLastError();
		printf("[-] ERROR: Param File VirtualAlloc error %i\n", err);
		CloseHandle(encFile);
		return 0;
	}
	if (pShellcode == NULL)
	{
		err = GetLastError();
		printf("[-] ERROR: Shell File VirtualAlloc error %i\n", err);
		CloseHandle(shellFile);
		return 0;
	}
	if (pEncCode2 == NULL)
	{
		err = GetLastError();
		printf("[-] ERROR: Empty Param VirtualAlloc error %i\n", err);
		CloseHandle(encFile);
		return 0;
	}

	printf("[+] Reading files...\n");

	DWORD nShellBytesRead = 0;
	DWORD nEncBytesRead = 0;
	DWORD nEncBytesRead2 = 0;

	ReadFile(shellFile, pShellcode, shellSize, &nShellBytesRead, NULL);
	CloseHandle(shellFile);
	printf("[+] ShellCode file read completed with %i/%i bytes.\n", shellSize, nShellBytesRead);

	ReadFile(encFile, pEncCode, encSize, &nEncBytesRead, NULL);
	CloseHandle(encFile);
	printf("[+] Param file read completed with %i/%i bytes.\n", encSize, nEncBytesRead);

	ReadFile(encFile2, pEncCode2, encSize2, &nEncBytesRead2, NULL);
	CloseHandle(encFile);
	printf("[+] Param file read completed with %i/%i bytes.\n", encSize, nEncBytesRead);

	int fileloc1 = static_cast<int>(reinterpret_cast<intptr_t>(pShellcode));
	int fileloc2 = static_cast<int>(reinterpret_cast<intptr_t>(pEncCode));
	int fileloc3 = static_cast<int>(reinterpret_cast<intptr_t>(pEncCode2));
	std::cout << "[+] ShellCode memory has been allocated (RWX) and code copied to: 0x" << std::hex << fileloc1 << std::endl;
	std::cout << "[+] Param memory has been allocated (RW) and code copied to: 0x" << std::hex << fileloc2 << std::endl;
	std::cout << "[+] Empty Result Space been allocated (RW) at the location: 0x" << std::hex << fileloc3 << std::endl;
	printf("[+] Pausing right before shell execution.  If needed, now would be the time to:\n");
	printf("   [+] Attach to this proess with x32dbg and set a bp on the shell memory region.\n");
	printf("   [+] Check allocted memory region contents with process hacker.\n");
	printf("[+] Enter any char and press enter to continue...\n");
	scanf_s(" %s", &hold, 2);


	printf("[+] Executing shellcode using CallWindowProc and passing param file as arg.\n");
	printf("[+] Hold on to your butts...\n");

	ret = CallWindowProcA((WNDPROC)pShellcode, (HWND)pEncCode, (UINT)pEncCode2, (WPARAM)encSize2, 0);

	printf("[+] Shellcode executed!\n");
	return ret;

}
