import subprocess
import os

def mov_merger(target_dir):
    #ターゲットフォルダに合わせて処理を実行
    input_text_path = os.path.join(target_dir,"_input.txt")

    ## ffmpegにおいて、concatするときはtxtにファイル名の一覧を載せる必要あり
    ## ファイル名の一覧は、txtから見た相対パス
    ## txtのパスは、スラッシュのみ利用可。windowsのときのバックスラッシュは、読み込みすらされない
    txt = open(input_text_path, 'w' , encoding='UTF-8')

    # 環境によっては、フォルダの配列が順番通りに読み込まれないので、一応ソートをかましておこう。
    tmp_path_list = os.listdir(target_dir)
    tmp_path_list.sort()
    for f in tmp_path_list:
      txt.write("file " + f.replace(os.sep,'/') + '\n')

    txt.close()

    output_mov_fullname = os.path.join(target_dir,"_merged.mp4")

    # ログレベルの設定で、エラーのみ出力するようにしてある。
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", input_text_path.replace(os.sep,'/'), "-c" ,  "copy", output_mov_fullname , "-loglevel" , "error" ])

    print("動画の結合が終了しました。_merged.mp4です。")