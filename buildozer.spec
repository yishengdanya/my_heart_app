[app]
title = HeartPopup
package.name = com.yourname.heartpopup
package.domain = com.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 不锁定 python3 版本，交由 android.python_version 控制
requirements = python3,kivy==2.2.1,cython==3.0.10

orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

# ---------- 权限与SDK ----------
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 30
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.gradle_dependencies = []

# ---------- 编译资源优化 ----------
android.memory_size = 4096
android.ndk_api = 24
android.jobs = 2

# ✅ 关键：指定 Python 版本为 3.10
android.python_version = 3.10

# 删除或注释掉下面这行（避免冲突）
# android.p4a_arguments = --python-version 3.10

[buildozer]
log_level = 2
warn_on_root = 1