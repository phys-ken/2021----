# 無音部分の抜きとり

## 参考
* [こちら](https://nantekottai.com/2020/06/14/video-cut-silence/)を参考に、無音部分の倍速処理のコードを書き加えました。
  * ※ ちなみに、リンク先のコードはちょびっとバグがあって、コピペしただけでは動かないのでご注意を...。

## 使い方
* `python douga_auto_trimer.py {動画の相対パス}`でコマンドラインから実行すると、動画の無音部分と有音部分に分けます。
* 無音部分の処理は、`douga_auto_trimer.py` の中のパラメーターを変更すれば、処理できます。

``````Python
# パラメータの設定 単位は__秒
padding_time = 0.2 #ブツ切れにならないように、有音部分の前後に幅を作る
thres = 0.05 # 音圧の閾値
min_silence_duration = 2 # 音のある最短感覚
min_keep_duration = 0.7 # ノイズのカット時間
baisoku = 8 # カット部分を何倍速にするか #baisoku = 0 で、倍速処理を行わず、無音部分はカットにする。

```````




## 環境
* python 3以上
* `pip install soundfile`
* ffmpegをインストールしておく必要がある。

## 参考にしたサイト
* [【ffmpeg】動画・音声を連結する concat の使い方 其の3](https://looooooooop.blog.fc2.com/blog-entry-1235.html)
* [ffmpegで変換の際に大量に出る標準出力をログレベル指定ですっきりする](https://yatta47.hateblo.jp/entry/2015/03/03/231204)