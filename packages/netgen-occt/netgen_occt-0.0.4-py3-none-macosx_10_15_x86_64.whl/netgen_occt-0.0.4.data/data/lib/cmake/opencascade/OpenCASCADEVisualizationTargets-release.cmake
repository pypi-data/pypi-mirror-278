#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "TKService" for configuration "Release"
set_property(TARGET TKService APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(TKService PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libTKService.7.8.2.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libTKService.7.8.2.dylib"
  )

list(APPEND _cmake_import_check_targets TKService )
list(APPEND _cmake_import_check_files_for_TKService "${_IMPORT_PREFIX}/lib/libTKService.7.8.2.dylib" )

# Import target "TKV3d" for configuration "Release"
set_property(TARGET TKV3d APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(TKV3d PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libTKV3d.7.8.2.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libTKV3d.7.8.2.dylib"
  )

list(APPEND _cmake_import_check_targets TKV3d )
list(APPEND _cmake_import_check_files_for_TKV3d "${_IMPORT_PREFIX}/lib/libTKV3d.7.8.2.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
