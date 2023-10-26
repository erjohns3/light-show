cmake_minimum_required(VERSION 3.21 FATAL_ERROR)

include(CMakeDependentOption)
include(CheckSymbolExists)

# Save the current source/binary dirs if we're in a subdirectory of a larger CMake project.
set(PROJECTM_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
set(PROJECTM_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}")

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED YES)
set(CMAKE_POSITION_INDEPENDENT_CODE YES)

# Don't export any symbols except those explicitly exported.
set(CMAKE_VISIBILITY_INLINES_HIDDEN YES)
set(CMAKE_C_VISIBILITY_PRESET hidden)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

option(ENABLE_DEBUG_POSTFIX "Add \"d\" (by default) after library names for debug builds." ON)
if(ENABLE_DEBUG_POSTFIX)
    set(CMAKE_DEBUG_POSTFIX "d" CACHE STRING "Output file debug postfix. Default is \"d\".")
endif()

project(libprojectM
        LANGUAGES C CXX
        VERSION 4.0.0
        )

# The API (SO) version for the shared library. Should be incremented whenever the binary interface changes
# in a non-backwards-compatible way, e.g. changing parameters or return values of existing functions or removing
# functions. Adding new function should be okay if documented.
set(PROJECTM_SO_VERSION "4")

# Base filename of all installed libraries. Also used as package name in pkgconfig.
set(PROJECTM_LIBRARY_BASE_OUTPUT_NAME "projectM-${PROJECT_VERSION_MAJOR}")

# The actual (full) library version of projectM
set(PROJECTM_LIB_VERSION "${CMAKE_PROJECT_VERSION}")

list(APPEND CMAKE_MODULE_PATH "${PROJECTM_SOURCE_DIR}/cmake")

include(GNUInstallDirs)

set(PROJECTM_BIN_DIR "${CMAKE_INSTALL_BINDIR}" CACHE STRING "Executable installation directory, relative to the install prefix.")
set(PROJECTM_LIB_DIR "${CMAKE_INSTALL_LIBDIR}" CACHE STRING "Library installation directory, relative to the install prefix.")
set(PROJECTM_INCLUDE_DIR "${CMAKE_INSTALL_INCLUDEDIR}" CACHE STRING "Header installation directory, relative to the install prefix.")

# Dummy file for merged static libs.
set(PROJECTM_DUMMY_SOURCE_FILE "${PROJECTM_BINARY_DIR}/dummy.cpp")
file(TOUCH "${PROJECTM_DUMMY_SOURCE_FILE}")

# Feature options, including dependencies.
option(BUILD_SHARED_LIBS "Build and install libprojectM as a shared libraries. If OFF, builds as static libraries." ON)
option(ENABLE_PLAYLIST "Enable building the playlist management library" ON)
option(ENABLE_SDL_UI "Build the SDL2-based developer test UI" OFF)
option(ENABLE_OPENMP "Enable OpenMP support if available" ON)
option(ENABLE_THREADING "Enable multithreading support." ON) # !TODO I CHANGED THIS
option(ENABLE_SYSTEM_GLM "Enable use of system-install GLM library" OFF)
option(ENABLE_GLES "Enable OpenGL ES support" ON)

# Experimental/unsupported features
option(ENABLE_LLVM "Enable experimental LLVM JIT support" OFF)

if(ENABLE_SYSTEM_GLM)
    find_package(GLM REQUIRED)
else()
    add_library(GLM::GLM INTERFACE IMPORTED)
    set_target_properties(GLM::GLM PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES "${PROJECTM_SOURCE_DIR}/vendor"
            )
endif()

if(ENABLE_SDL_UI)
    execute_process(COMMAND hostname OUTPUT_VARIABLE HOSTNAME OUTPUT_STRIP_TRAILING_WHITESPACE)
    if("${HOSTNAME}" STREQUAL "doorbell")
        message(STATUS "HOSTNAME IS DOORBELL!")
    else()
        message(STATUS "HOSTNAME IS NOTTTTT DOORBELL!")
        find_package(SDL2 REQUIRED)
    endif()
endif()


# find_package(OpenGL REQUIRED COMPONENTS GLES2)
# find_package(OpenGL REQUIRED COMPONENTS GLES2)
# find_package(OpenGL REQUIRED COMPONENTS GLES3 PATHS /usr/lib/aarch64-linux-gnu)

if(ENABLE_GLES)
    message(STATUS "Building for OpenGL Embedded Profile")
    # We use a local find script for OpenGL::GLES3 until the proposed changes are merged upstream.
    # list(APPEND CMAKE_MODULE_PATH "${PROJECTM_SOURCE_DIR}/cmake/gles")
    

    execute_process(COMMAND hostname OUTPUT_VARIABLE HOSTNAME OUTPUT_STRIP_TRAILING_WHITESPACE)
    if("${HOSTNAME}" STREQUAL "doorbell")
        message(STATUS "HOSTNAME IS DOORBELL!")
        add_library(OpenGL::GLES3 INTERFACE IMPORTED)
        target_include_directories(OpenGL::GLES3 INTERFACE /usr/include/GLES3/)
        target_link_libraries(OpenGL::GLES3 INTERFACE /usr/lib/aarch64-linux-gnu/libGLESv2.so)    
    else()
        message(STATUS "HOSTNAME IS NOTTTTT DOORBELL!")
        find_package(OpenGL REQUIRED COMPONENTS GLES3)
    endif()

    if(NOT TARGET OpenGL::GLES3)
        message(FATAL_ERROR "No suitable GLES3 library was found.")
    endif()

    set(PROJECTM_OPENGL_LIBRARIES OpenGL::GLES3)
    set(USE_GLES ON)
else()
    message(STATUS "Building for OpenGL Core Profile")
    find_package(OpenGL REQUIRED)
    set(PROJECTM_OPENGL_LIBRARIES OpenGL::GL)
    # GLX is required by SOIL2 on platforms with the X Window System (e.g. most Linux distributions)
    if(TARGET OpenGL::GLX)
        list(APPEND PROJECTM_OPENGL_LIBRARIES OpenGL::GLX)
    endif()
endif()

if(ENABLE_OPENMP)
    find_package(OpenMP)
    if(NOT OpenMP_FOUND OR NOT OpenMP_CXX_FOUND)
        set(ENABLE_OPENMP OFF)
    endif()
endif()

if(ENABLE_THREADING)
    find_package(Threads REQUIRED)
    set(PROJECTM_USE_THREADS YES)
endif()

if(ENABLE_LLVM)
    find_package(LLVM REQUIRED)
    if(LLVM_VERSION VERSION_LESS 10.0)
        message(FATAL_ERROR "LLVM JIT support requires at least version 10.0, but only ${LLVM_VERSION} was found.")
    endif()
    set(HAVE_LLVM TRUE)
else()
    unset(HAVE_LLVM)
endif()

set(CMAKE_C_VISIBILITY_PRESET hidden)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)

include(features.cmake)

add_subdirectory(presets)
add_subdirectory(vendor)
add_subdirectory(src)

message(STATUS "")
message(STATUS "libprojectM v${PROJECT_VERSION}")
message(STATUS "==============================================")
message(STATUS "")
message(STATUS "    prefix:                  ${CMAKE_INSTALL_PREFIX}")
message(STATUS "    libdir:                  ${PROJECTM_LIB_DIR}")
message(STATUS "    includedir:              ${PROJECTM_INCLUDE_DIR}")
message(STATUS "    bindir:                  ${PROJECTM_BIN_DIR}")
message(STATUS "")
message(STATUS "    compiler:                ${CMAKE_CXX_COMPILER}")
message(STATUS "    cflags:                  ${CMAKE_C_FLAGS}")
message(STATUS "    cxxflags:                ${CMAKE_CXX_FLAGS}")
message(STATUS "    ldflags:                 ${CMAKE_SHARED_LINKER_FLAGS}")
message(STATUS "")
message(STATUS "Features:")
message(STATUS "==============================================")
message(STATUS "")
message(STATUS "    Build shared libraries:  ${BUILD_SHARED_LIBS}")
message(STATUS "    Threading:               ${ENABLE_THREADING}")
message(STATUS "    SDL2:                    ${ENABLE_SDL_UI}")
message(STATUS "    USE_GLES:                    ${USE_GLES}")
if(ENABLE_SDL_UI)
    message(STATUS "        SDL2 version:        ${SDL2_VERSION}")
endif()
message(STATUS "    OpenGL ES:               ${ENABLE_GLES}")
message(STATUS "    OpenMP:                  ${ENABLE_OPENMP}")
if(ENABLE_OPENMP)
    message(STATUS "        OpenMP version:      ${OpenMP_CXX_VERSION}")
endif()
message(STATUS "    LLVM JIT:                ${ENABLE_LLVM}")
if(ENABLE_LLVM)
    message(STATUS "        LLVM version:        ${LLVM_VERSION}")
endif()
message(STATUS "    Use system GLM:          ${ENABLE_SYSTEM_GLM}")
message(STATUS "    Link UI with shared lib: ${ENABLE_SHARED_LINKING}")
message(STATUS "")
message(STATUS "Targets and applications:")
message(STATUS "==============================================")
message(STATUS "")
message(STATUS "    libprojectM:             (always built)")
message(STATUS "    Playlist library:        ${ENABLE_PLAYLIST}")
message(STATUS "    SDL2 Test UI:            ${ENABLE_SDL_UI}")
message(STATUS "    Tests:                   ${BUILD_TESTING}")
message(STATUS "")

# Create CPack configuration
set(CPACK_PACKAGE_NAME "projectM")
set(CPACK_VERBATIM_VARIABLES YES)
include(CPack)
