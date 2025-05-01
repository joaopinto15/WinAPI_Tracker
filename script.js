// == Configuration: list of WinAPI functions to hook ==
const api_list = [
    "NtOpenThread", "ExitWindowsEx", "FindResourceW", "CryptExportKey", "CreateRemoteThreadEx", "MessageBoxTimeoutW",
    "InternetCrackUrlW", "StartServiceW", "GetFileSize", "GetVolumeNameForVolumeMountPointW", "GetFileInformationByHandle",
    "CryptAcquireContextW", "RtlDecompressBuffer", "SetWindowsHookExA", "RegSetValueExW", "LookupAccountSidW",
    "SetUnhandledExceptionFilter", "InternetConnectA", "GetComputerNameW", "RegEnumValueA", "NtOpenFile", "NtSaveKeyEx",
    "HttpOpenRequestA", "recv", "GetFileSizeEx", "LoadStringW", "SetInformationJobObject", "WSAConnect", "CryptDecrypt",
    "GetTimeZoneInformation", "InternetOpenW", "CoInitializeEx", "CryptGenKey", "GetAsyncKeyState", "NtQueryInformationFile",
    "GetSystemMetrics", "NtDeleteValueKey", "NtOpenKeyEx", "sendto", "IsDebuggerPresent", "RegQueryInfoKeyW",
    "NetShareEnum", "InternetOpenUrlW", "WSASocketA", "CopyFileExW", "connect", "ShellExecuteExW", "SearchPathW",
    "GetUserNameA", "InternetOpenUrlA", "LdrUnloadDll", "EnumServicesStatusW", "EnumServicesStatusA", "WSASend",
    "CopyFileW", "NtDeleteFile", "CreateActCtxW", "timeGetTime", "MessageBoxTimeoutA", "CreateServiceA", "FindResourceExW",
    "WSAAccept", "InternetConnectW", "HttpSendRequestA", "GetVolumePathNameW", "RegCloseKey", "InternetGetConnectedStateExW",
    "GetAdaptersInfo", "shutdown", "NtQueryMultipleValueKey", "NtQueryKey", "GetSystemWindowsDirectoryW", "GlobalMemoryStatusEx",
    "GetFileAttributesExW", "OpenServiceW", "getsockname", "LoadStringA", "UnhookWindowsHookEx", "NtCreateUserProcess",
    "Process32NextW", "CreateThread", "LoadResource", "GetSystemTimeAsFileTime", "SetStdHandle", "CoCreateInstanceEx",
    "GetSystemDirectoryA", "NtCreateMutant", "RegCreateKeyExW", "IWbemServices_ExecQuery", "NtDuplicateObject", "Thread32First",
    // ... TRUNCATED: You can paste the entire list from your JSON here ...
    "NtReadFile" // last function in your list
];

const output_path = "C:\Users\pinto\github\PESTI-WORK\wazuh\wazuh-agent\frida_logs\frida_api_sequence.json";
const max_calls = 100;

// DLLs to search for APIs
const dll_list = [
    "ntdll.dll",
    "kernel32.dll",
    "user32.dll",
    "advapi32.dll",
    "ws2_32.dll",
    "wininet.dll",
    "crypt32.dll",
    "ole32.dll",
    "shell32.dll"
];
let sequence = [];

function flushSequence() {
    if (sequence.length === 0) return;

    send(sequence);
    sequence = [];
}
// == Hooking Logic ==
function hook_api(api_name) {
    for (let dll of dll_list) {
        const addr = Module.findExportByName(dll, api_name);
        if (addr !== null) {
            Interceptor.attach(addr, {
                onEnter: function (args) {
                    sequence.push(api_name);
                    if (sequence.length >= max_calls) {
                        flushSequence();
                    }
                }
            });
            return;
        }
    }
}

// Start hooking all APIs
for (let api_name of api_list) {
    hook_api(api_name);
}

console.log("[*] API hooking script loaded!")