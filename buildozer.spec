[app]
title = HeartPopup
package.name = com.yourname.heartpopup
package.domain = com.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 核心修复：移除 --no-deps 后，必须显式加上 cython 依赖以支持编译
requirements = python3,kivy,cython

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

# ---------- 内存和线程 ----------
android.memory_size = 2048
android.ndk_api = 24
android.jobs = 2

# 🟢 必看：之前导致失败的元凶就是这个参数！
# 请保证这一行后面绝对没有任何内容，留空即可！
android.p4a_arguments = 

[buildozer]
log_level = 2
warn_on_root = 1