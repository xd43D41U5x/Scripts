#include <iostream>
#include <sstream>
#include <cstdlib>
#include <time.h>
#include <Windows.h>
#include <fstream>
#include <vector>


int main()
{
    int secondXor = 0;

    std::string fileName;
    std::cout << "What is the name of the file: ";
    std::cin >> fileName;
    std::ifstream file(fileName, std::ios::binary);

    //reading the file content
    std::vector<char> buffer((std::istreambuf_iterator<char>(file)),
        (std::istreambuf_iterator<char>()));

    file.close();

    int bufSize = buffer.size();


    while(secondXor != 0xFC){
   
        //Seed for rand with current time.
        int curTime = time(0);
        srand(curTime);

        //Call rand and perform algorithm operations.
        int rndNum = rand() % 0x1e + 0x64 + 0x1ac52;

        //Use first random number as a seed for rand.
        srand(rndNum);

        //Perform first XOR operation on the current byte val using new rand number and algorithm.
        int rndValue = rand();
        int firstXor = (rndValue % 0x3c4 ^ buffer[0]) + 0x1;

        //Second round of XOR with the known random number.
        //Mask to mimic lower register DL operation.
        secondXor = (firstXor ^ rndNum) & 0x0ff;

        //Print Current value
        std::cout << "Current value is: ";
        std::cout << std::hex << secondXor << std::endl;

        if (secondXor == 0xFC)
        {
            std::cout << "[*] Found starting byte value of: " << secondXor << std::endl;
            std::cout << "[*] The correct time value was: " << std::hex << curTime << std::endl;
            std::cout << "[*] The random number seed was: " << rndNum << std::endl;
            std::cout << "[*] The resulting rand value was: " << rndValue << std::endl;
            std::cout << "[*] The first found XOR value was: " << firstXor << std::endl;
            std::cout << "[*] Starting decrypt with these values and writing to file..." << std::endl;

            //Open a file for writing and write the first known character.
            std::fstream fileOut;
            fileOut.open("out.bin", std::ios_base::out | std::ios_base::binary);
            fileOut.write(reinterpret_cast<char*>(&secondXor), 1);
            int pos = 1;
            while (pos < 0x3c4) {
                //Run similar algorithm as before for the rest of the data and write out.
                int newrand = rand();
                int firstX = (((newrand % 0x3c4 + 0x1)^ buffer[pos]) ) & 0x0ff;
                int secondX = (firstX ^ rndNum) & 0x0ff;
                fileOut.write(reinterpret_cast<char*>(&secondX), 1);
                pos++;
            }
            fileOut.close();
        }
        //Sleep for 1 second so we actually get good time seed values.
        Sleep(1000);
    }  
}
