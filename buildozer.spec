[app]
title = HeartPopup
package.name = com.yourname.heartpopup
package.domain = com.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

# ---------- 权限与SDK ----------
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 30
android.ndk = 25b
android.sdk = 30
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.gradle_dependencies = []

# ---------- 终极防崩溃保底配置 ----------
android.memory_size = 512
android.ndk_api = 24
android.jobs = 1

# 🟢 新增：彻底打断 pip 越界寻找包的环节
android.p4a_arguments = --no-deps --ignore-setup-py

[buildozer]
log_level = 2
warn_on_root = 1