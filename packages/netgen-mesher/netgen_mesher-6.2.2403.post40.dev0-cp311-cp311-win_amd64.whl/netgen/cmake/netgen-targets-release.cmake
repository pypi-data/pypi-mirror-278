#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ngcore" for configuration "Release"
set_property(TARGET ngcore APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngcore PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/netgen/lib/ngcore.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/netgen/ngcore.dll"
  )

list(APPEND _cmake_import_check_targets ngcore )
list(APPEND _cmake_import_check_files_for_ngcore "${_IMPORT_PREFIX}/netgen/lib/ngcore.lib" "${_IMPORT_PREFIX}/netgen/ngcore.dll" )

# Import target "nggui" for configuration "Release"
set_property(TARGET nggui APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nggui PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/netgen/lib/libnggui.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/netgen/libnggui.dll"
  )

list(APPEND _cmake_import_check_targets nggui )
list(APPEND _cmake_import_check_files_for_nggui "${_IMPORT_PREFIX}/netgen/lib/libnggui.lib" "${_IMPORT_PREFIX}/netgen/libnggui.dll" )

# Import target "ngpy" for configuration "Release"
set_property(TARGET ngpy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngpy PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/./netgen/libngpy.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./netgen/libngpy.pyd"
  )

list(APPEND _cmake_import_check_targets ngpy )
list(APPEND _cmake_import_check_files_for_ngpy "${_IMPORT_PREFIX}/./netgen/libngpy.lib" "${_IMPORT_PREFIX}/./netgen/libngpy.pyd" )

# Import target "ngguipy" for configuration "Release"
set_property(TARGET ngguipy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngguipy PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/./netgen/libngguipy.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./netgen/libngguipy.pyd"
  )

list(APPEND _cmake_import_check_targets ngguipy )
list(APPEND _cmake_import_check_files_for_ngguipy "${_IMPORT_PREFIX}/./netgen/libngguipy.lib" "${_IMPORT_PREFIX}/./netgen/libngguipy.pyd" )

# Import target "togl" for configuration "Release"
set_property(TARGET togl APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(togl PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/netgen/lib/togl.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/netgen/togl.dll"
  )

list(APPEND _cmake_import_check_targets togl )
list(APPEND _cmake_import_check_files_for_togl "${_IMPORT_PREFIX}/netgen/lib/togl.lib" "${_IMPORT_PREFIX}/netgen/togl.dll" )

# Import target "nglib" for configuration "Release"
set_property(TARGET nglib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nglib PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/netgen/lib/nglib.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/netgen/nglib.dll"
  )

list(APPEND _cmake_import_check_targets nglib )
list(APPEND _cmake_import_check_files_for_nglib "${_IMPORT_PREFIX}/netgen/lib/nglib.lib" "${_IMPORT_PREFIX}/netgen/nglib.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
