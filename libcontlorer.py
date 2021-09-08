import os
import subprocess

# 相対パスのリストを作っておく
paths = [
"input_mov/007_1_公式解説.mp4",
"input_mov/007_2_電場と電位.mp4",
"input_mov/007_3_高さ.mp4",
"input_mov/007_4_練習問題.mp4"
]


for p in paths:
  subprocess.run(["python" , "douga_auto_trimer.py" , p])

print("以下の動画の処理が終わりました！！！********************")
print(paths)