# -*- mode: python ; coding: utf-8 -*-
"""
Runtime hook to set LD_LIBRARY_PATH for bundled libraries.
This ensures that lanelet2 and autoware_lanelet2_extension_python 
libraries can find their dependencies at runtime.
"""
import os
import sys

# Get the runtime directory where PyInstaller extracts files
if getattr(sys, 'frozen', False):
    runtime_dir = sys._MEIPASS
else:
    runtime_dir = os.path.dirname(os.path.abspath(__file__))

# Add library paths - both root and module-specific subdirectories
library_paths = [
    runtime_dir,  # Root directory where bundled .so files are
    os.path.join(runtime_dir, 'lanelet2'),
    os.path.join(runtime_dir, 'autoware_lanelet2_extension_python'),
]

# Add existing LD_LIBRARY_PATH
existing_ld_library_path = os.environ.get('LD_LIBRARY_PATH', '')
if existing_ld_library_path:
    library_paths.append(existing_ld_library_path)

os.environ['LD_LIBRARY_PATH'] = ':'.join(library_paths)

# Also set RPATH-like behavior by ensuring libraries can be found via sys.path manipulation
# This helps with dlopen() calls that use relative paths
if getattr(sys, 'frozen', False):
    sys.path.insert(0, runtime_dir)
    sys.path.insert(0, os.path.join(runtime_dir, 'lanelet2'))
    sys.path.insert(0, os.path.join(runtime_dir, 'autoware_lanelet2_extension_python'))

