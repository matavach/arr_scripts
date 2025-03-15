#!/usr/bin/python
from time import strftime, localtime
import sys
import os
import ffmpeg

def error_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def log(text):
    time = strftime("%Y_%m_%d_%I_%M_%p", localtime())
    logfile = "/config/logs/m4b_split-" + author + "-" + book + "-" + time + ".txt"
    with open(logfile, "w",encoding="utf-8") as bookfile :
        bookfile.write(text)
    error_print(text)


# Use readarr vars if ran by readarr, otherwise use args
if "readarr_author_name" in os.environ :
    author = os.environ["readarr_author_name"]
    book = os.environ["readarr_book_title"]
    path = os.environ["readarr_author_path"] + "/" + book
else:
    path = sys.argv[1]
    author = path.split("/")[-2]
    book = path.split("/")[-1]


files = os.scandir(path)
m4b = []
for file in files :
    if file.name.endswith(".m4b") :
        print(file.name)
        m4b.append(file.path)

if len(m4b) > 1 :
    log(book + "is already split into multiple files")
    exit()

m4b = m4b[0]

ffprobe = ffmpeg.probe(m4b, cmd="ffprobe", show_chapters="-show_chapters")

chapters = ffprobe.get('chapters')

if chapters is None:
    log(book + "has no chapters.")
    exit()


i = 0
for chapter in chapters:
    i = i + 1
    new_title = author + " - " + book + f" {i:03}" + ".m4b"
    new_path = path + "/" + new_title
    audio = ffmpeg.input(m4b,ss=chapter.get("start_time"),to=chapter.get("end_time")).audio
    output = ffmpeg.output(audio,new_path,acodec='copy',map_chapters="-1")
    output.run(quiet=True)
