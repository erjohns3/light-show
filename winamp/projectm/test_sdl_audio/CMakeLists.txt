# rm CMakeCache.txt; cmake -DCMAKE_BUILD_TYPE=Release && cmake --build . && ./test_sdl2


# on doorbell
    # rm CMakeCache.txt; cmake -DCMAKE_BUILD_TYPE=Release && cmake --build . && LD_LIBRARY_PATH=/home/pi/random/sdl_install/SDL/build/.libs/ ./test_sdl2


cmake_minimum_required(VERSION 3.21 FATAL_ERROR)

project(test_sdl2 LANGUAGES C CXX)

set(BIN_DIR "." CACHE STRING "Executable installation directory, relative to the install prefix.")
set(LIB_DIR "." CACHE STRING "Library installation directory, relative to the install prefix.")
set(INCLUDE_DIR "." CACHE STRING "Header installation directory, relative to the install prefix.")

add_executable(test_sdl2 test_sdl.cpp)


execute_process(COMMAND hostname OUTPUT_VARIABLE HOSTNAME OUTPUT_STRIP_TRAILING_WHITESPACE)
if("${HOSTNAME}" STREQUAL "doorbell")
    message(STATUS "HOSTNAME IS DOORBELL!")
    target_include_directories(test_sdl2 PRIVATE BEFORE "/home/pi/random/sdl_install/SDL-release-2.28.4/")
    target_link_libraries(test_sdl2
        PRIVATE
        /home/pi/random/sdl_install/SDL-release-2.28.4/build/.libs/libSDL2.so
        ${CMAKE_DL_LIBS}
    )
else()
    message(STATUS "HOSTNAME IS NOTTTTT DOORBELL!")
    find_package(SDL2 REQUIRED)
    target_link_libraries(test_sdl2
        PRIVATE
        SDL2::SDL2
        ${CMAKE_DL_LIBS}
    )
endif()

message(STATUS "        SDL2 version:        ${SDL2_VERSION}")



# find_package(glfw3 REQUIRED)

# get_target_property(_SDL2_INCLUDE_DIR SDL2::SDL2 INTERFACE_INCLUDE_DIRECTORIES)
# if(_SDL2_INCLUDE_DIR MATCHES "(.+)/SDL2\$" AND _SDL2_TARGET_TYPE STREQUAL STATIC_LIBRARY)
#     # Check if SDL2::SDL2 is aliased to SDL2::SDL2-static (will be the case for static-only builds)
#     get_target_property(_SDL2_ALIASED_TARGET SDL2::SDL2 ALIASED_TARGET)
#     if(_SDL2_ALIASED_TARGET)
#         set(_sdl2_target ${_SDL2_ALIASED_TARGET})
#     else()
#         set(_sdl2_target SDL2::SDL2)
#     endif()

#     message(STATUS "SDL2 include dir contains \"SDL2\" subdir (SDL bug #4004) - fixing to \"${CMAKE_MATCH_1}\".")
#     set_target_properties(${_sdl2_target} PROPERTIES
#             INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_MATCH_1}"
#             )
# endif()

if(SDL2_VERSION AND SDL2_VERSION VERSION_LESS "2.0.5")
    message(FATAL_ERROR "SDL2 libraries were found, but have version ${SDL2_VERSION}. At least version 2.0.5 is required.")
endif()




