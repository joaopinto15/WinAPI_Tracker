#include "utils.hpp"
#include <Windows.h>
#include <TlHelp32.h>
#include <iostream>

int Error(const char* msg) {
    std::cout << "[+] Error: " << msg << " " << GetLastError() << std::endl;
    return 1;
}

std::wstring GetProcessName(uint32_t pid) {
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnap == INVALID_HANDLE_VALUE) return L"<Error>";

    PROCESSENTRY32 pe32 = { sizeof(PROCESSENTRY32) };
    if (!Process32First(hSnap, &pe32)) {
        CloseHandle(hSnap);
        return L"<Error>";
    }

    do {
        if (pid == pe32.th32ProcessID) {
            CloseHandle(hSnap);
            return pe32.szExeFile;
        }
    } while (Process32Next(hSnap, &pe32));

    CloseHandle(hSnap);
    return L"<Error>";
}
