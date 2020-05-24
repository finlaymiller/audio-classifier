import argparse
import parse_file
import sys
import os
import json
import time
import logging
import watchdog
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

parser = argparse.ArgumentParser(description='Automatically classify audio files')
parser.add_argument('path_to_watch', type=str, help='Folder to watch for incoming audio')

def on_created(event):
	print(f"Classifying {event.src_path}")
	time.sleep(5)
	parse_file.process_file(event.src_path)

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

def clf_all_files_r():
	rootdir = "B:\Documents\Programming\Datasets\FSDKaggle2019"
	outfilename = 'FSDclassifications.json'
	classes = dict()

	for root, dirs, files in os.walk(rootdir, topdown=False):
		for f in files:
			print("Classifying ", f)
			time.sleep(1)
			samplerate, shape, preds = parse_file.process_file(os.path.join(root, f))
			if samplerate != 0:
				classes[f] = []
				classes[f].append({
					"Sample Rate": samplerate,
					"Shape": shape,
					"Predictions": preds
				})

				with open(outfilename, 'w') as outfile:
					print("Writing classification to file...")
					json.dump(classes, outfile, indent='\t')



if __name__ == "__main__":
	args = parser.parse_args()
	clf_all_files_r()
	#watcher(**vars(args))
