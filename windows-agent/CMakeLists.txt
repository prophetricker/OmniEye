cmake_minimum_required(VERSION 3.20)

project(omnieye_windows_agent LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CAMERA_SDK_ROOT "" CACHE PATH "Path to CameraSDK-*-win64 directory")

if(NOT CAMERA_SDK_ROOT)
    message(FATAL_ERROR "Set CAMERA_SDK_ROOT to the extracted CameraSDK win64 directory")
endif()

add_executable(omnieye_windows_agent src/main.cpp)

target_include_directories(omnieye_windows_agent PRIVATE
    "${CAMERA_SDK_ROOT}/include"
)

target_link_libraries(omnieye_windows_agent PRIVATE
    "${CAMERA_SDK_ROOT}/lib/CameraSDK.lib"
)

add_custom_command(TARGET omnieye_windows_agent POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${CAMERA_SDK_ROOT}/bin/CameraSDK.dll"
        "$<TARGET_FILE_DIR:omnieye_windows_agent>/CameraSDK.dll"
)
