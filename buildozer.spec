[app]
title = HeartPopup
package.name = com.yourname.heartpopup
package.domain = com.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 🟢 最终绝杀：锁定 Python 3.11，升级 Kivy 2.3.1，彻底避开 cgi 缺失的坑！
requirements = python3==3.11.9,kivy==2.3.1,cython==3.0.10

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

# ---------- 编译资源优化 ----------
android.memory_size = 2048
android.ndk_api = 24
android.jobs = 2

# 🟢 绝对不能有任何参数，留空
android.p4a_arguments = 

[buildozer]
log_level = 2
warn_on_root = 1