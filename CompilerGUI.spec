
from kivy_deps import sdl2, glew
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['CompilerGUI.py'],
             pathex=['D:\\ASU Engineering Career\\2-Junior year\\Semester 2\\Design of Compilers\\Project 3'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz, Tree('D:\\ASU Engineering Career\\2-Junior year\\Semester 2\\Design of Compilers\\Project 3\\'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          [],
          name='CompilerGUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
