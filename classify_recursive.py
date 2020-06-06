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


def classify(rootdir, outfilename):

	for root, dirs, files in os.walk(rootdir, topdown=False):
		for f in files:
			classes = {}
			print("Classifying \'{}\'".format(f))
			time.sleep(0.5)
			samplerate, shape, preds = parse_file.process_file(os.path.join(root, f))
			if samplerate != 0:
				classes[f] = {
					"Filename": f,
					"Sample Rate": samplerate,
					"Length": shape[0],
					"Predictions": preds
				}

				with open(outfilename, 'a') as o:
					print("Writing classification to \'{}\'".format(o))
					json.dump(classes[f], o)
					o.write('\n')


if __name__ == "__main__":
	args = parser.parse_args()
	classify(args.path_to_classify, args.outfile_name)
