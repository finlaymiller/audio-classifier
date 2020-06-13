import argparse
import sys
import os
import json
import time
import logging
import watchdog
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import parse_file


class NewFile(FileSystemEventHandler):

	valid_extensions = {
		'.mp3',
		'.wav'
	}

	file = {
		'full': '',
		'name': '',
		'ext': ''
	}


	def __init__(self, path, outfile, v):
		self.path = path
		self.outfile = outfile
		self.v = v

	def process(self, event):
		if event.is_directory:
			return
    
		if self.file['ext'] in self.valid_extensions:
			print("Classifying \'{}\'".format(self.file['name']))
			# time.sleep(0.5)
			samplerate, shape, preds = parse_file.process_file(self.file['full'], self.v)

			classes = {}
			if samplerate != 0:
				classes[self.file['name']] = {
					"Sample Rate": samplerate,
					"Length": shape[0],
					"Predictions": dict(preds)
				}

				with open(self.outfile, 'a') as o:
					if self.v is True:
						print("Writing classification to \'{}\'".format(self.outfile))
					# the o.write()s below are so that the data is written in the
					# JSON Lines format
					o.write('{{\"{}\": '.format(self.file['name']))
					json.dump(classes[self.file['name']], o)
					o.write('}}\n')
			print('Done writing classification, waiting for next file')


	def on_created(self, event):
		# wait for file to finish transferring
		historicalSize = -1
		while (historicalSize != os.path.getsize(event.src_path)):
			historicalSize = os.path.getsize(event.src_path)
			time.sleep(0.1)
		# save file info
		self.file['full'] = os.path.basename(event.src_path)
		self.file['name'], self.file['ext'] = os.path.splitext(self.file['full'])
		# classify file
		self.process(event)


def watch(path_to_watch, outfilename, v=False):
	event_handler = NewFile(path_to_watch, outfilename, v)
	observer = Observer()
	observer.schedule(event_handler, path_to_watch, recursive=True)

	if v is True:
		print("Watching \'{}\' for new files\nPress Ctrl+C at any time to exit".format(path_to_watch))
		time.sleep(3)
		logging.basicConfig(level=logging.INFO,
												format='[ %(asctime)s - %(message)s ]',
												datefmt='%Y-%m-%d %H:%M:%S')
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
