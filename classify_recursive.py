import argparse
import parse_file
import sys
import os
import json
import time
import logging

parser = argparse.ArgumentParser(description='Automatically classify audio files in a folder')
parser.add_argument('path_to_classify', type=str, 
					help='Folder containing audio to classify')
parser.add_argument('outfile_name', type=str, 
					help='Name of file to write classifications to (must be JSON).')


def clf_all_files_r():
	rootdir = args.path_to_classify
	outfilename = args.outfile_name
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
