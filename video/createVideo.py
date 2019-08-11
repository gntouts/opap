import os
os.system("mkdir vid")
os.system("ffmpeg -r 9 -f image2 -s 1920x1080 -i ./img/%d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p ./vid/raw.mp4")
