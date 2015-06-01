# -*- mode: python -*-
a = Analysis(['D:\\Workspace\\LDA\\analysis\\Nexus.py'],
             pathex=['D:\\Workspace\\LDA\\exporter'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Nexus.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
