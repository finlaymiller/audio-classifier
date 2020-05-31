import argparse
import parse_file
import sys
import time
import logging
import watchdog
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

parser = argparse.ArgumentParser(description='Automatically classify audio files')
parser.add_argument('path_to_watch', type=str, help='Folder to watch for incoming audio')

def on_created(event):
    print(f"Classifying {event.src_path}")
    time.sleep(1)
    _, _, _ = parse_file.process_file(event.src_path)

def watcher(path_to_watch = '.'):
    print("Starting watcher...")
    logging.basicConfig(level=logging.INFO,
                        format='[ %(asctime)s - %(message)s ]',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    path = path_to_watch
    event_handler = LoggingEventHandler()
    event_handler.on_created = on_created
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
	args = parser.parse_args()
	watcher(**vars(args))