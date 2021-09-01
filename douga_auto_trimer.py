<<<<<<< HEAD
import sys

args = sys.argv


input_mov_path = args[1]
=======
input_mov_path = ""
>>>>>>> efc4de7725356d09dbc91379d01fcbff87f8764a

import subprocess
logs = subprocess.run(["ffmpeg", "-i", input_mov_path ,  "-ac" , "1" , "-ar" ,  "44100", "-acodec",  "pcm_s16le", "_tmp.wav" ,  "-y"])
print(logs)

import soundfile as sf
import os
import numpy as np
from matplotlib import pyplot as plt
import time
import faster
import datetime

# パラメータの設定 単位は__秒
padding_time = 0.2 #ブツ切れにならないように、無音の幅を作る
thres = 0.05 # 音圧の閾値
min_silence_duration = 2 # 音のある最短感覚
min_keep_duration = 0.7 # ノイズのカット時間
baisoku = 8 # カット部分を何倍速にするか #baisoku = 0 で、倍速処理を行わず、無音部分はカットにする。



print("無音カットの処理を始めます。")
src_file = os.path.join("./", "_tmp.wav")

data, samplerate = sf.read(src_file)
t = np.arange(0, len(data))/samplerate
fig = plt.figure(figsize=(18, 6))
plt.plot(t, data)
print("音源の読み込みに成功しました。分析します...")
fig.savefig("_tmp.png")

# 閾値より大きいのがb
amp = np.abs(data)
b = amp > thres

print("音声の波形データを分析しました。スライスを始めます。")
# 閾値をもとに、スライスをする。

silences = []
prev = 0
entered = 0
for i, v in enumerate(b):
  if prev == 1 and v == 0: # enter silence
    entered = i
  if prev == 0 and v == 1: # exit silence
    duration = (i - entered) / samplerate 
    if duration > min_silence_duration:
      silences.append({"from": entered, "to": i, "suffix": "cut"})
      entered = 0
  prev = v
if entered > 0 and entered < len(b):
  silences.append({"from": entered, "to": len(b), "suffix": "cut"})

# 短いノイズを除去

cut_blocks = []
blocks = silences
while 1:
  if len(blocks) <= 1:
    try:
        cut_blocks.append(blocks[0])
    except:
        pass
    break
  
  block = blocks[0]
  next_blocks = [block]
  for i, b in enumerate(blocks):
    if i == 0:
      continue
    interval = (b["from"] - block["to"]) / samplerate
    if interval < min_keep_duration:
      block["to"] = b["to"]
      next_blocks.append(b)

  cut_blocks.append(block)
  blocks = list(filter(lambda b: b not in next_blocks, blocks))
    
print(cut_blocks)

# 残すところの配列に変える

keep_blocks = []
for i, block in enumerate(cut_blocks):
  if i == 0 and block["from"] > 0:
    keep_blocks.append({"from": 0, "to": block["from"], "suffix": "keep"})
  if i > 0:
    prev = cut_blocks[i - 1]
    keep_blocks.append({"from": prev["to"], "to": block["from"], "suffix": "keep"})
  if i == len(cut_blocks) - 1 and block["to"] < len(data):
    keep_blocks.append({"from": block["to"], "to": len(data), "suffix": "keep"})

all_blocks = keep_blocks

print("残す部分を決めました。")


# 出力範囲をグラフで吐く
fig = plt.figure(figsize=(18, 6))
ax = fig.add_subplot(111)
plt.plot(t, amp)

for st in all_blocks:
  print(str(st["from"]) + ":" +str(st["to"]))
  ax.axvspan(st["from"]/samplerate, st["to"] / samplerate, color = "coral")


fig.savefig("_tmp2.png") 



# time = 0　が、keepかcutか判断する
if all_blocks[0]["from"] == 0:
  first_keep = True
  keep_top = 0
  cut_top = 1
else:
  first_keep = False
  keep_top = 1
  cut_top = 0



# フォルダ作成
now = datetime.datetime.now()
current_time = now.strftime("%Y-%m-%d-%H-%M")
filename = os.path.basename(input_mov_path)
out_dir = os.path.join("./", "auto_trimed", current_time + "_" + filename )
os.makedirs(out_dir,exist_ok = True)


# 残す部分を出力
for i, block in enumerate(all_blocks):
  fr = max(block["from"] / samplerate - padding_time, 0)
  to = min(block["to"] / samplerate + padding_time, len(data) / samplerate)
  duration = to - fr
  out_path = os.path.join(out_dir, "{}_{}_{}.mp4".format(str(i).zfill(4), keep_top,block["suffix"]))
  print(out_path + " --- " + str(block["from"]) + ":" + str(block["to"]))
  subprocess.run(["ffmpeg", "-ss", str(fr) ,"-i" ,input_mov_path , "-t" , str(duration) , out_path])


# 斬る部分を出力
for i, block in enumerate(cut_blocks):
  fr = max(block["from"] / samplerate + padding_time, 0)
  to = min(block["to"] / samplerate - padding_time, len(data) / samplerate)
  duration = to - fr
  out_path = os.path.join(out_dir, "{}_{}_{}.mp4".format(str(i).zfill(4), cut_top,block["suffix"]))
  print(out_path + " --- " + str(block["from"]) + ":" + str(block["to"]))
  subprocess.run(["ffmpeg", "-ss", str(fr) ,"-i" ,input_mov_path , "-t" , str(duration) , out_path])


# cut部分の
for f in os.listdir(out_dir):
  if "cut" in f:
    input_filepath = os.path.join(out_dir,f)
    print(input_filepath)
    faster.mov_faster(input_filepath,baisoku = baisoku)

print("作業が終了しました")