#include <windows.h>
#include <iostream>

int main()
{
    HINSTANCE hGetProcIDDLL = LoadLibrary(L"C:\\test.dll");

    if (!hGetProcIDDLL) {
        std::cout << "could not load the dynamic library" << std::endl;
        return EXIT_FAILURE;
    }

    getchar();

}
