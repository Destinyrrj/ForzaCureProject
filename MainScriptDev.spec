# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    [r'C:\Python\FH\ForzaCureProject\MainScriptDev.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['psutil', 'subprocess', 'logging', 'webbrowser', 'time', 'warnings', 'tkinter', 'json', 'os'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ForzaCure_a14Dev',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[r'C:\Users\kosti\Downloads\icons8-forza-horizon-4-64.ico'],
)