from os import pathconf_names
import subprocess

# 相対パスのリストを作っておく
paths = [
"004/004_1_練習問題まで.mp4",
"004/004_2練習問題解説.mp4",
"004/004_3電荷の公式_Trim.mp4",
"004/004_4点電荷の場合.mp4",
"004/004_5例題1.mp4",
"004/004_06_例題2.mp4"
]


for p in paths:
  subprocess.run(["python" , "handler/douga_auto_trimer.py" , p])

print("以下の動画の処理が終わりました！！！********************")
print(paths)