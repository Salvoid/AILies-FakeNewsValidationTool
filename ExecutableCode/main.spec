# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/admin/Desktop/collegeTemp/BSCS 4-1 (2nd Semester)/003_COSC-E4 CS Elective 4 Machine Learning/FinalRequirement/Tasks/002_Software/ExecutableCode/gui_module.py', '.'), ('C:/Users/admin/Desktop/collegeTemp/BSCS 4-1 (2nd Semester)/003_COSC-E4 CS Elective 4 Machine Learning/FinalRequirement/Tasks/002_Software/ExecutableCode/fetcher_module.py', '.'), ('C:/Users/admin/Desktop/collegeTemp/BSCS 4-1 (2nd Semester)/003_COSC-E4 CS Elective 4 Machine Learning/FinalRequirement/Tasks/002_Software/ExecutableCode/process_module.py', '.'), ('C:/Users/admin/Desktop/collegeTemp/BSCS 4-1 (2nd Semester)/003_COSC-E4 CS Elective 4 Machine Learning/FinalRequirement/Tasks/002_Software/ExecutableCode/other_module.py', '.'), ('C:/Users/admin/Desktop/collegeTemp/BSCS 4-1 (2nd Semester)/003_COSC-E4 CS Elective 4 Machine Learning/FinalRequirement/Tasks/002_Software/ExecutableCode/assets', 'assets'), ('C:/Users/admin/AppData/Local/Programs/Python/Python310/Lib/site-packages/scipy.libs', 'scipy.libs/'), ('C:/Users/admin/AppData/Local/Programs/Python/Python310/Lib/site-packages/seaborn', 'seaborn/'), ('C:/Users/admin/AppData/Local/Programs/Python/Python310/Lib/site-packages/matplotlib.libs', 'matplotlib.libs/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
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
    icon='window_icon.ico',
)
