cmake_minimum_required(VERSION 3.15)
project(WinAPI_Tracker)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable Unicode
add_definitions(-DUNICODE -D_UNICODE)

# Include directories
include_directories(include)
include_directories(include/krabs)  # KrabsETW headers are here

# Source files
file(GLOB SOURCES
    src/*.cpp
)

# Create executable
add_executable(WinAPI_Tracker ${SOURCES})

# Link necessary Windows libraries
target_link_libraries(WinAPI_Tracker
    advapi32
    kernel32
    user32
    psapi
    version
)

# Set output directory (optional)
set_target_properties(WinAPI_Tracker PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
