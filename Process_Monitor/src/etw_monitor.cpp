#include "etw_monitor.hpp"
#include "injector.hpp"
#include "utils.hpp"
#include <krabs.hpp>
#include <iostream>

void begin_trace() {
    krabs::user_trace trace;
    krabs::provider<> provider(L"Microsoft-Windows-Kernel-Process");
    provider.any(0x10);

    auto callback = [](const EVENT_RECORD& record, const krabs::trace_context& ctx) {
        krabs::schema schema(record, ctx.schema_locator);
        krabs::parser parser(schema);

        uint32_t ppid = parser.parse<uint32_t>(L"ParentProcessID");
        std::wstring image_name = parser.parse<std::wstring>(L"ImageName");

        if (image_name.find(L"\\Device\\HarddiskVolume3\\malwareSample") == 0) {
            uint32_t pid = parser.parse<uint32_t>(L"ProcessID");
            std::wcout << L"[!] Process Found in Tracking Area Detected\n";
            inject_dll(pid);
        } else if (ppid != record.EventHeader.ProcessId) {
            uint32_t pid = parser.parse<uint32_t>(L"ProcessID");
            std::wcout << L"[!] Process PPID Spoofing Detected\n";
            inject_dll(pid);
        }
    };

    krabs::event_filter filter(krabs::predicates::id_is(1));
    filter.add_on_event_callback(callback);
    provider.add_filter(filter);
    trace.enable(provider);
    trace.start();
}
