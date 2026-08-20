[app]
title = HeartPopup
package.name = com.yourname.heartpopup
package.domain = com.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 🟢 终极绝杀：不锁定Python版本（避免和容器环境冲突），直接拉取Kivy官方最新源码分支（内含Python 3.14的cgi补丁）
requirements = python3,kivy @ git+https://github.com/kivy/kivy.git@master,cython

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

# 🟢 绝不能有任何多余参数，保持空置
android.p4a_arguments = 

[buildozer]
log_level = 2
warn_on_root = 1