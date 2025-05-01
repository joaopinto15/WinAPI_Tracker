#include "injector.hpp"
#include "config.hpp"
#include <Windows.h>
#include <iostream>
#include <vector>
#include <filesystem>

void inject_dll(uint32_t pid) {
    std::wstring injector_path = get_executable_directory() + L"\\injector.exe";

    if (!std::filesystem::exists(injector_path)) {
        std::wcerr << L"[!] Injector script not found: " << injector_path << std::endl;
        return;
    }

    std::wstring command_line = L"\"" + injector_path + L"\" " + std::to_wstring(pid);

    STARTUPINFOW si = { sizeof(si) };
    PROCESS_INFORMATION pi = { 0 };

    std::vector<wchar_t> cmdline(command_line.begin(), command_line.end());
    cmdline.push_back(0);

    if (CreateProcessW(NULL, cmdline.data(), NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        std::wcout << L"[+] Injector launched successfully." << std::endl;
    } else {
        std::wcerr << L"[!] Failed to start injector. Error: " << GetLastError() << std::endl;
    }
}
