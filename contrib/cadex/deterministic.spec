# -*- mode: python -*-
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules


for i, x in enumerate(sys.argv):
    if x == '--name':
        cmdline_name = sys.argv[i+1]
        break
else:
    raise Exception('no name')

hiddenimports = collect_submodules('trezorlib')
hiddenimports += collect_submodules('safetlib')
hiddenimports += collect_submodules('btchip')
hiddenimports += collect_submodules('keepkeylib')
hiddenimports += collect_submodules('websocket')
hiddenimports += [
    'electrum_cadex',
    'electrum_cadex.base_crash_reporter',
    'electrum_cadex.base_wizard',
    'electrum_cadex.plot',
    'electrum_cadex.qrscanner',
    'electrum_cadex.websockets',
    'electrum_cadex.gui.qt',
    'PyQt5.sip',

    'electrum_cadex.plugins',

    'electrum_cadex.plugins.hw_wallet.qt',

    'electrum_cadex.plugins.audio_modem.qt',
    'electrum_cadex.plugins.cosigner_pool.qt',
    'electrum_cadex.plugins.digitalbitbox.qt',
    'electrum_cadex.plugins.email_requests.qt',
    'electrum_cadex.plugins.keepkey.qt',
    'electrum_cadex.plugins.revealer.qt',
    'electrum_cadex.plugins.labels.qt',
    'electrum_cadex.plugins.trezor.client',
    'electrum_cadex.plugins.trezor.qt',
    'electrum_cadex.plugins.safe_t.client',
    'electrum_cadex.plugins.safe_t.qt',
    'electrum_cadex.plugins.ledger.qt',
    'electrum_cadex.plugins.virtualkeyboard.qt',
]

datas = [
    ('electrum_cadex/servers.json', 'electrum_cadex'),
    ('electrum_cadex/servers_testnet.json', 'electrum_cadex'),
    ('electrum_cadex/servers_regtest.json', 'electrum_cadex'),
    ('electrum_cadex/currencies.json', 'electrum_cadex'),
    ('electrum_cadex/checkpoints.json', 'electrum_cadex'),
    ('electrum_cadex/locale', 'electrum_cadex/locale'),
    ('electrum_cadex/wordlist', 'electrum_cadex/wordlist'),
    ('C:\\zbarw', '.'),
]
datas += collect_data_files('trezorlib')
datas += collect_data_files('safetlib')
datas += collect_data_files('btchip')
datas += collect_data_files('keepkeylib')

# Add libusb so Trezor and Safe-T mini will work
binaries = [('C:/Python36/libusb-1.0.dll', '.')]
binaries += [('C:/x11_hash/libx11hash-0.dll', '.')]
binaries += [('C:/libsecp256k1/libsecp256k1.dll', '.')]

# https://github.com/pyinstaller/pyinstaller/wiki/Recipe-remove-tkinter-tcl
sys.modules['FixTk'] = None
excludes = ['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter']
excludes += [
    'PyQt5.QtBluetooth',
    'PyQt5.QtCLucene',
    'PyQt5.QtDBus',
    'PyQt5.Qt5CLucene',
    'PyQt5.QtDesigner',
    'PyQt5.QtDesignerComponents',
    'PyQt5.QtHelp',
    'PyQt5.QtLocation',
    'PyQt5.QtMultimedia',
    'PyQt5.QtMultimediaQuick_p',
    'PyQt5.QtMultimediaWidgets',
    'PyQt5.QtNetwork',
    'PyQt5.QtNetworkAuth',
    'PyQt5.QtNfc',
    'PyQt5.QtOpenGL',
    'PyQt5.QtPositioning',
    'PyQt5.QtQml',
    'PyQt5.QtQuick',
    'PyQt5.QtQuickParticles',
    'PyQt5.QtQuickWidgets',
    'PyQt5.QtSensors',
    'PyQt5.QtSerialPort',
    'PyQt5.QtSql',
    'PyQt5.Qt5Sql',
    'PyQt5.Qt5Svg',
    'PyQt5.QtTest',
    'PyQt5.QtWebChannel',
    'PyQt5.QtWebEngine',
    'PyQt5.QtWebEngineCore',
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebKit',
    'PyQt5.QtWebKitWidgets',
    'PyQt5.QtWebSockets',
    'PyQt5.QtXml',
    'PyQt5.QtXmlPatterns',
    'PyQt5.QtWebProcess',
    'PyQt5.QtWinExtras',
]

a = Analysis(['electrum-cadex'],
             hiddenimports=hiddenimports,
             datas=datas,
             binaries=binaries,
             excludes=excludes,
             runtime_hooks=['pyi_runtimehook.py'])

# http://stackoverflow.com/questions/19055089/
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='icons/electrum-cadex.ico',
          name=os.path.join('build\\pyi.win32\\electrum', cmdline_name))

# exe with console output
conexe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          debug=False,
          strip=False,
          upx=False,
          console=True,
          icon='icons/electrum-cadex.ico',
          name=os.path.join('build\\pyi.win32\\electrum',
                            'console-%s' % cmdline_name))

# trezorctl separate executable
tctl_a = Analysis(['C:/Python36/Scripts/trezorctl'],
                  hiddenimports=[
                    'pkgutil',
                    'win32api',
                  ],
                  excludes=excludes,
                  runtime_hooks=['pyi_tctl_runtimehook.py'])

tctl_pyz = PYZ(tctl_a.pure)

tctl_exe = EXE(tctl_pyz,
           tctl_a.scripts,
           exclude_binaries=True,
           debug=False,
           strip=False,
           upx=False,
           console=True,
           name=os.path.join('build\\pyi.win32\\electrum', 'trezorctl.exe'))

coll = COLLECT(exe, conexe, #tctl_exe,
               a.binaries,
               a.datas,
               strip=False,
               upx=False,
               name=os.path.join('dist', 'electrum-cadex'))
