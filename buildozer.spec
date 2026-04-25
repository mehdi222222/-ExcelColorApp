[app]

title = ExcelColorApp
package.name = excelcolorapp
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,xlsx

version = 1.0

requirements = python3,kivy,openpyxl

orientation = portrait
fullscreen = 0

android.api = 30
android.minapi = 21
android.arch = armeabi-v7a

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

[buildozer]

log_level = 2
warn_on_root = 1

