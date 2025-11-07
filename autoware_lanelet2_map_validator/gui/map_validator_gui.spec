# -*- mode: python ; coding: utf-8 -*-
import os
import glob
import sys
import importlib.util
import subprocess

def get_module_path(module_name):
    """Get the file path of an imported module."""
    spec = importlib.util.find_spec(module_name)
    if spec and spec.origin:
        return os.path.dirname(spec.origin)
    return None

def get_library_dependencies(sofile):
    """Get all shared library dependencies of a .so file using ldd."""
    try:
        output = subprocess.check_output(['ldd', sofile], stderr=subprocess.DEVNULL, text=True)
        deps = []
        for line in output.split('\n'):
            line = line.strip()
            if '=>' in line and 'not found' not in line:
                parts = line.split('=>')
                if len(parts) > 1:
                    path_part = parts[1].strip().split()[0]
                    if path_part.startswith('/') and os.path.exists(path_part):
                        deps.append(path_part)
        return deps
    except:
        return []

# Collect binaries and data files
binaries = []
datas = []
discovered_libs = set()

# Find and add lanelet2 module files
lanelet2_path = get_module_path('lanelet2')
if lanelet2_path:
    # Add .so files as binaries (required for runtime linking)
    for sofile in glob.glob(os.path.join(lanelet2_path, '**/*.so*'), recursive=True):
        if os.path.islink(sofile) or os.path.isfile(sofile):
            rel_path = os.path.relpath(sofile, lanelet2_path)
            target_dir = os.path.join('lanelet2', os.path.dirname(rel_path))
            binaries.append((sofile, target_dir))
            discovered_libs.add(os.path.basename(sofile))
            
            # Also discover and bundle dependencies
            for dep in get_library_dependencies(sofile):
                if dep not in discovered_libs:
                    dep_name = os.path.basename(dep)
                    binaries.append((dep, '.'))
                    discovered_libs.add(dep)
    
    # Add Python files
    for pyfile in glob.glob(os.path.join(lanelet2_path, '**/*.py'), recursive=True):
        rel_path = os.path.relpath(pyfile, lanelet2_path)
        target_dir = os.path.join('lanelet2', os.path.dirname(rel_path))
        datas.append((pyfile, target_dir))

# Find and add autoware_lanelet2_extension_python module files
ext_python_path = get_module_path('autoware_lanelet2_extension_python')
if ext_python_path:
    # Add .so files as binaries (they depend on lanelet2)
    for sofile in glob.glob(os.path.join(ext_python_path, '**/*.so*'), recursive=True):
        if os.path.islink(sofile) or os.path.isfile(sofile):
            rel_path = os.path.relpath(sofile, ext_python_path)
            target_dir = os.path.join('autoware_lanelet2_extension_python', os.path.dirname(rel_path))
            binaries.append((sofile, target_dir))
            discovered_libs.add(os.path.basename(sofile))
            
            # Also discover and bundle dependencies
            for dep in get_library_dependencies(sofile):
                if dep not in discovered_libs:
                    dep_name = os.path.basename(dep)
                    binaries.append((dep, '.'))
                    discovered_libs.add(dep)
    
    # Add Python files
    for pyfile in glob.glob(os.path.join(ext_python_path, '**/*.py'), recursive=True):
        rel_path = os.path.relpath(pyfile, ext_python_path)
        target_dir = os.path.join('autoware_lanelet2_extension_python', os.path.dirname(rel_path))
        datas.append((pyfile, target_dir))

a = Analysis(
    ['gui.py'],
    pathex=[''],
    binaries=binaries,
    datas=datas,
    hiddenimports=['lanelet2', 'lanelet2.io', 'autoware_lanelet2_extension_python', 'autoware_lanelet2_extension_python.projection'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook_libpath.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='autoware_lanelet2_map_validator_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
