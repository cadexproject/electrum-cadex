Index: Electrum-CADEX-3.2.3/setup.py
===================================================================
--- Electrum-CADEX-3.2.3.orig/setup.py
+++ Electrum-CADEX-3.2.3/setup.py
@@ -77,6 +77,7 @@ setup(
         'electrum_cadex',
         'electrum_cadex.gui',
         'electrum_cadex.gui.qt',
+        'electrum_cadex.plugins',
     ] + [('electrum_cadex.plugins.'+pkg) for pkg in find_packages('electrum_cadex/plugins')],
     package_dir={
         'electrum_cadex': 'electrum_cadex'
