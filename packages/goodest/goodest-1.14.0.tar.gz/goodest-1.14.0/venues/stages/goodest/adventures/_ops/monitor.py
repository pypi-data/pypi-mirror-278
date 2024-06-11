



'''
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen

class RestartHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f'Restarting Sanic due to change in {event.src_path}')
        os.execl(sys.executable, sys.executable, *sys.argv)

def watch_changes():
    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_sanic():
    Popen(['python', 'your_sanic_app.py'])

if __name__ == '__main__':
    run_sanic()
    watch_changes()

'''