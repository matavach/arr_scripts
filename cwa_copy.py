#!/usr/bin/python
from time import strftime, localtime, sleep
import sys
import os
import shutil
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers.polling import PollingObserver
import subprocess
Done = False

log_text = list()
if "readarr_eventtype" in os.environ :
    if os.environ["readarr_eventtype"] == "Test" :
        print(os.environ["readarr_eventtype"])
        exit()

def log(text):
    time = strftime("%Y_%m_%d_%I_%M_%p", localtime())
    # title = (author + "_" + book).replace(" ", "_").replace(".","")
    title = "test"
    logfile = "/config/logs/cwa_copy_"  + time + "_" + title + ".txt"
    with open(logfile, "w",encoding="utf-8") as bookfile :
        bookfile.write('\n'.join(text))

# # Use readarr vars if ran by readarr, otherwise use args
# if "readarr_author_name" in os.environ :
#     author = os.environ["readarr_author_name"]
#     book = os.environ["readarr_book_title"]
#     path = os.environ["readarr_author_path"] + "/" + book
# else:
#     path = sys.argv[1]
#     author = path.split("/")[-2]
#     book = path.split("/")[-1]


# files = os.scandir(path)

# for file in files:
#     shutil.copy(file.path, "/transcode/cwa")

# log_text.append(author + " - " + book + " successfully copied to 'Calibre ingest' folder")

file_name = ""

class BookWatch(FileSystemEventHandler):
    patterns = [".epub"]
        
    def on_created(self, event):
        print("in")
        self._is_paused = True
        
        # WAITING FOR FILE TRANSFER
        file = None
        while file is None:
            try:
                file = open(event.src_path)
            except OSError:
                file = None                    
                sleep(1) # WAITING FOR FILE TRANSFER
                continue
        global file_name
        file_name = file.name
        self.observer.stop() 

event_handler = BookWatch()
obs = PollingObserver()

obs.schedule(event_handler, "/data/media/books/calibre", recursive=True)
event_handler.observer = obs
obs.start()

print("starting observer")

try:
    while obs.is_alive():
        print("while loop")
        obs.join()
finally:
    obs.stop()
    obs.join()


result = subprocess.run(["/root/go/bin/kindle-send", "-config", "/config/scripts/KindleConfig.json", "-file", f"{file_name}"], capture_output=True, text=True)
print(result)
log_text.append(result)
log(log_text)
