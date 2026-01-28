#include <windows.h>
#include <iostream>
#include <winternl.h> 
#include <vector>


#pragma comment(lib, "ntdll.lib") 


typedef NTSTATUS(WINAPI* PNtQueryInformationProcess)(
    HANDLE ProcessHandle,
    PROCESSINFOCLASS ProcessInformationClass,
    PVOID ProcessInformation,
    ULONG ProcessInformationLength,
    PULONG ReturnLength
    );

int main() {

    wchar_t buffer[] = L"powershell.exe lakdjflakjglakdjflakjglakdjflakjglakdjflakjglakdjflakjglakdjflakjg";
    LPWSTR lpwstr = buffer;
    STARTUPINFOW si = { sizeof(si) };
    PROCESS_INFORMATION pi = { 0 };

    BOOL successCProc = CreateProcessW(NULL, buffer, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL, NULL, &si, &pi);

    if (successCProc) {
        std::cout << "Process created! PID: " << pi.dwProcessId << std::endl;
        std::cout << "Process is currently suspended." << std::endl;

        PNtQueryInformationProcess NtQueryInformationProcess =
            (PNtQueryInformationProcess)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtQueryInformationProcess");

        if (NtQueryInformationProcess == NULL) {
            std::cerr << "Failed to get NtQueryInformationProcess address." << std::endl;
            return 1;
        }

        PROCESS_BASIC_INFORMATION pbi;
        ULONG returnLength = 0;
        NTSTATUS status = NtQueryInformationProcess(pi.hProcess, ProcessBasicInformation, &pbi, sizeof(PROCESS_BASIC_INFORMATION), &returnLength);

        if (status != 0) {
            std::cerr << "NtQueryInformationProcess failed." << std::endl;
            return 1;
        }

        PEB peb;
        SIZE_T bytesRead = 0;
        //Initial read to get PEB
        BOOL success = ReadProcessMemory(pi.hProcess, pbi.PebBaseAddress, &peb, sizeof(PEB), &bytesRead);

        if (!success) {
            std::cerr << "ReadProcessMemory failed. Error: " << GetLastError() << std::endl;
            return 1;
        }

        PUNICODE_STRING remoteCmdLine = &((PRTL_USER_PROCESS_PARAMETERS)peb.ProcessParameters)->CommandLine;

        std::cout << "Successfully read PEB." << std::endl;
        std::cout << "PEB Base Address: 0x" << std::hex << pbi.PebBaseAddress << std::endl;
        std::cout << "Proc Params Base Addy: " << remoteCmdLine << std::endl;


        UNICODE_STRING us;
        //Read again to get cmd line
        if (!ReadProcessMemory(pi.hProcess, remoteCmdLine, &us, sizeof(us), NULL)) {
            std::cerr << "ReadProcessMemory failed. Error: " << GetLastError() << std::endl;
            return 1;
        }

        std::cout << "CmdLine read successful with length: " << us.Length << std::endl;

        //By putting write-host at the end, there is no need to update the size as long as it is shorter then the initial.
        std::wstring newString = L"powershell.exe New-Item -Path hiThere.txt -ItemType File;write-host ";

        USHORT newByteLen = static_cast<USHORT>(newString.length() * sizeof(wchar_t));

        //Write new string
        if (!WriteProcessMemory(pi.hProcess, us.Buffer, newString.c_str(), newByteLen, NULL)) return 1;

        
        ResumeThread(pi.hThread);

        //Clean up handles
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }
    else {
        std::cerr << "Failed to create process. Error: " << GetLastError() << std::endl;
    }
    
}
