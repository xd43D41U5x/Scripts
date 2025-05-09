// For dlls that use the entrypoint/dllmain for malicious code, there are times you have to use something like LoadLibrary so that the functions will return and the dll stays running.
// This very simple program will allow that but will also give a good way to break on dll entry in x64dbg.
// Place in the same directory as your dll and make sure it is named payload.dll.

#include <iostream>
#include <windows.h>

int main()
{
    std::cout << "Running dll...\n";
    LPCWSTR dllPath = L"payload.dll";
    HINSTANCE hinstLib = LoadLibraryW(dllPath);
    Sleep(INFINITE);
    return 0;
}
