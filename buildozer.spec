[app]
title = HeartPopup
package.name = com.yourname.heartpopup
package.domain = com.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 🟢 绝杀锁定：不指定Python版本，锁定Kivy 2.2.1 和 Cython 3.0.10 防编译塌方
requirements = python3,kivy==2.2.1,cython==3.0.10

orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

# ---------- 权限与SDK ----------
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 30
# 🔴 满足工具最低要求的 NDK 版本
android.ndk = 25b
# android.sdk 已废弃，在此处删除
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.gradle_dependencies = []

# ---------- 编译资源优化 ----------
# 内存加大，防被杀
android.memory_size = 4096
android.ndk_api = 24
# 注意：这里的 jobs 后面会被环境变量覆盖，写多少都行
android.jobs = 2

# 🟢 保持空置，绝不能再写 --no-deps 等参数
android.p4a_arguments = 

[buildozer]
log_level = 2
warn_on_root = 1