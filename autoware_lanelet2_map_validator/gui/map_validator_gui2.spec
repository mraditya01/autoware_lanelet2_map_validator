# -*- mode: python ; coding: utf-8 -*-
import os
import glob
import sys
import importlib.util

def get_module_path(module_name):
    """Get the file path of an imported module."""
    spec = importlib.util.find_spec(module_name)
    if spec and spec.origin:
        return os.path.dirname(spec.origin)
    return None

# Collect binaries and data files
binaries = []
datas = []

# Find and add lanelet2 module files
lanelet2_path = get_module_path('lanelet2')
if lanelet2_path:
    print(f"[PyInstaller] Found lanelet2 at: {lanelet2_path}", file=sys.stderr)
    # Add .so files as binaries (required for runtime linking)
    for sofile in glob.glob(os.path.join(lanelet2_path, '**/*.so*'), recursive=True):
        rel_path = os.path.relpath(sofile, lanelet2_path)
        dest_dir = os.path.join('lanelet2', os.path.dirname(rel_path))
        binaries.append((sofile, dest_dir))
        print(f"[PyInstaller] Bundling lanelet2 binary: {sofile} -> {dest_dir}", file=sys.stderr)
    # Add Python files
    for pyfile in glob.glob(os.path.join(lanelet2_path, '**/*.py'), recursive=True):
        rel_path = os.path.relpath(pyfile, lanelet2_path)
        dest_dir = os.path.join('lanelet2', os.path.dirname(rel_path))
        datas.append((pyfile, dest_dir))
else:
    print("[PyInstaller] WARNING: lanelet2 module not found!", file=sys.stderr)

# Find and add autoware_lanelet2_extension_python module files
ext_python_path = get_module_path('autoware_lanelet2_extension_python')
if ext_python_path:
    print(f"[PyInstaller] Found autoware_lanelet2_extension_python at: {ext_python_path}", file=sys.stderr)
    # Add .so files as binaries
    for sofile in glob.glob(os.path.join(ext_python_path, '**/*.so*'), recursive=True):
        rel_path = os.path.relpath(sofile, ext_python_path)
        dest_dir = os.path.join('autoware_lanelet2_extension_python', os.path.dirname(rel_path))
        binaries.append((sofile, dest_dir))
        print(f"[PyInstaller] Bundling autoware_lanelet2_extension_python binary: {sofile} -> {dest_dir}", file=sys.stderr)
    # Add Python files
    for pyfile in glob.glob(os.path.join(ext_python_path, '**/*.py'), recursive=True):
        rel_path = os.path.relpath(pyfile, ext_python_path)
        dest_dir = os.path.join('autoware_lanelet2_extension_python', os.path.dirname(rel_path))
        datas.append((pyfile, dest_dir))
else:
    print("[PyInstaller] WARNING: autoware_lanelet2_extension_python module not found!", file=sys.stderr)

print(f"[PyInstaller] Total binaries to bundle: {len(binaries)}", file=sys.stderr)
print(f"[PyInstaller] Total data files to bundle: {len(datas)}", file=sys.stderr)

a = Analysis(
    ['gui.py'],
    pathex=[''],
    binaries=binaries,
    datas=datas,
    hiddenimports=['lanelet2', 'lanelet2.io', 'autoware_lanelet2_extension_python', 'autoware_lanelet2_extension_python.projection'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook_ld_library_path.py'],
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
