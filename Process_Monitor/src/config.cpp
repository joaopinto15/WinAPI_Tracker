#include "config.hpp"
#include <Windows.h>
#include <iostream>
#include <filesystem>

std::wstring config_path;

std::wstring get_executable_directory() {
    wchar_t buffer[MAX_PATH];
    GetModuleFileNameW(NULL, buffer, MAX_PATH);
    std::wstring path(buffer);
    return path.substr(0, path.find_last_of(L"\\/"));
}

std::wstring get_config_value(const std::wstring& section, const std::wstring& key, const std::wstring& default_value) {
    wchar_t buffer[512];
    GetPrivateProfileStringW(section.c_str(), key.c_str(), default_value.c_str(), buffer, 512, config_path.c_str());
    return std::wstring(buffer);
}

bool load_config() {
    config_path = get_executable_directory() + L"\\config.ini";

    if (!std::filesystem::exists(config_path)) {
        std::wcerr << L"[!] config.ini not found at: " << config_path << std::endl;
        return false;
    }

    std::wstring monitored_folder = get_config_value(L"monitor", L"monitored_folder");
    if (monitored_folder.empty()) {
        std::wcerr << L"[!] 'monitored_folder' not found or empty in config.ini" << std::endl;
        return false;
    }

    std::wcout << L"[+] Monitoring folder: " << monitored_folder << std::endl;
    return true;
}
