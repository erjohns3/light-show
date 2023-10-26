set(projectM-Eval_VERSION 1.0.0)


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was projectM-EvalConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

set(_projectM-Eval_FIND_PARTS_REQUIRED)
if(projectM-Eval_FIND_REQUIRED)
    set(_projectM-Eval_FIND_PARTS_REQUIRED REQUIRED)
endif()
set(_projectM-Eval_FIND_PARTS_QUIET)
if(projectM-Eval_FIND_QUIETLY)
    set(_projectM-Eval_FIND_PARTS_QUIET QUIET)
endif()

include("${CMAKE_CURRENT_LIST_DIR}/projectM-EvalTargets.cmake")

if(projectM-Eval_FIND_COMPONENTS)
    foreach(component ${projectM-Eval_FIND_COMPONENTS})
        find_package(projectM-Eval${component}
            ${_projectM-Eval_FIND_PARTS_REQUIRED}
            ${_projectM-Eval_FIND_PARTS_QUIET}
            )

        if(NOT projectM-Eval${component}_FOUND)
            if (projectM-Eval_FIND_REQUIRED_${component})
                set(_projectM-Eval_NOTFOUND_MESSAGE "${_projectM-Eval_NOTFOUND_MESSAGE}Failed to find projectM-Eval component \"${component}\" config file\n")
            elseif(NOT projectM-Eval_FIND_QUIETLY)
                message(WARNING "Failed to find projectM-Eval component \"${component}\" config file")
            endif()
        endif()
    endforeach()
endif()

if (_projectM-Eval_NOTFOUND_MESSAGE)
    set(projectM-Eval_NOT_FOUND_MESSAGE "${_projectM-Eval_NOTFOUND_MESSAGE}")
    set(projectM-Eval_FOUND False)
endif()
