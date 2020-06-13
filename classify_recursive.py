import argparse
import parse_file
import sys
import os
import json
import time
import logging


def classify(rootdir, outfilename, v=False):

	for root, dirs, files in os.walk(rootdir, topdown=False):
		for f in files:
			classes = {}
			if v is True:
				print("Classifying \'{}\'".format(f))
			time.sleep(0.5)
			samplerate, shape, preds = parse_file.process_file(os.path.join(root, f), v)
			if samplerate != 0:
				classes[f] = {
					"Sample Rate": samplerate,
					"Length": shape[0],
					"Predictions": dict(preds)
				}

				with open(outfilename, 'a') as o:
					if v is True:
						print("Writing classification to \'{}\'".format(outfilename))
					# the o.write()s below are so that the data is written in the
					# JSON Lines format
					o.write('{{\"{}\": '.format(f))
					json.dump(classes[f], o)
					o.write('}}\n')
