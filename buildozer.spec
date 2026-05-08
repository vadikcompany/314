[app]

# (str)
title = Hybrid Chat

# (str)
package.name = hybridchat

# (str)
package.domain = org.test

# (str)
source.dir = .

# (list)
source.include_exts = py,png,jpg,kv,atlas

# (str)
version = 0.1

# (list)
requirements = python3,kivy==2.3.0

# (str)
orientation = portrait

# (list)
# INTERNET
android.permissions = INTERNET, WAKE_LOCK
android.archs = arm64-v8a

# (int)
android.api = 31

# (int)
android.sdk = 31

# (int)
android.minapi = 21

# (bool)
fullscreen = 0

# (str) Android build-tools version to use
android.build_tools_version = 31.0.0

[buildozer]
# (int)
log_level = 2

# (str)
bin_dir = ./bin
