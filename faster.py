import subprocess
import os

def mov_faster(input_file , baisoku = 4):
    dirname = os.path.dirname(input_file)
    basename_without_ext = os.path.splitext(os.path.basename(input_file))[0]
    ext = os.path.splitext(os.path.basename(input_file))[1]
    output_file = os.path.join( dirname ,  basename_without_ext + "_fast" + ext)

    if not baisoku == 0:
        subprocess.run([ "ffmpeg", "-i", input_file, "-vf" ,  "setpts=PTS/" + str(baisoku) , "-af" , "aresample=48000,asetrate=48000*" + str(baisoku) ,  "-ar", "48000", output_file  , "-y" , "-loglevel" , "quiet"] , stdout=subprocess.DEVNULL)

    os.remove(input_file)