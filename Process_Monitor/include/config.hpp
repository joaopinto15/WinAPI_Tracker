#pragma once
#include <string>

bool load_config();
std::wstring get_executable_directory();
std::wstring get_config_value(const std::wstring& section, const std::wstring& key, const std::wstring& default_value = L"");
