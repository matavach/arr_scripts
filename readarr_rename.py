#!/usr/bin/python
from time import strftime, localtime
import sys
import os
import ffmpeg

readarr = False

if((sys.argv[1]).count("/") > 1):
    path = sys.argv[1]
else:
    path = os.getcwd() + "/" + sys.argv[1]

author = path.split("/")[-2]
book = path.split("/")[-1]

files = os.scandir(path)


i = 1
names= []
for file in files:
    if file.name.endswith(".mp3") or file.name.endswith(".m4b"):
        names.append(file.name)



for name in sorted(names):
    new_title = author + " - " + book + f" {i:03}" + ".m4b"
    os.rename((path+ "/" +name),(path+"/"+new_title))
    print(new_title)
    i+=1