[app]
title = HeartPopup
package.name = com.yourname.heartpopup
package.domain = com.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 核心修复：锁定极稳定版本组合，彻底解决 expected 6 have 5 编译崩溃
requirements = python3,kivy==2.2.1,cython==3.0.10

orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

# ---------- 权限与SDK ----------
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 30
# 修复：从 25b 降级为 23b，避开 NDK 与 Python3.14 的交叉编译冲突
android.ndk = 23b
android.sdk = 30
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.gradle_dependencies = []

# ---------- 编译资源优化 ----------
android.memory_size = 2048
android.ndk_api = 24
android.jobs = 2

# 🟢 绝对关键：此参数必须绝对留空！不要再填任何内容！
android.p4a_arguments = 

[buildozer]
log_level = 2
warn_on_root = 1