import argparse
import datetime
import logging
import os
import sys

import classify_live as live
import classify_recursive as recursive

parser = argparse.ArgumentParser(description='Automatically classify audio files in a folder')
parser.add_argument('-l', '--live', action='store_true', 
	help='Start a watcher to classify files as they are added to a folder')
parser.add_argument('-p', '--path', type=str, default='./', 
	help='Folder containing audio to classify')
parser.add_argument('-o', '--outfile', type=str,
	help='Name of file to write classifications to (must be JSON). If none is specified, the classifications will be written to \'classifications_[TIMESTAMP].json\'')
parser.add_argument('-v', '--verbose', action='store_true', 
	help='Control classifier output level. Some prints will always be printed (e.g. tensorflow warnings)')

outfile = 'YouShouldNeverSeeThisFile.txt'

def auto_classify():
	global outfile

	if args.live is False:
		recursive.classify(args.path, outfile, args.verbose)
	else:
		live.watch(args.path, outfile, args.verbose)


def verify_args():
	global outfile

	# check validity of input path
	if args.path and not os.path.isdir(args.path):
		print("Invalid folder to classify: \'{}\'\nExiting...".format(args.path))
		exit()

	if not args.outfile:
		outfile = 'classifications_{:%Y%m%d%H%M%S}.json'.format(datetime.datetime.now())
	else:		
		if os.path.exists(args.outfile):
			print("The classifier will only write it's output to new files. Please specify a file that does not yet exist")
			exit()
		else:
			outfile = args.outfile

	# print arguments if verbose is activated
	if args.verbose:
		if args.live is True:
			print("Classifying in live mode")
		else:
			print("Classifying in one-shot mode, files added after this will not be classified")
		print("Classifying files in location: \'{}\'".format(args.path))
		print("Outputting classifications to: \'{}\'".format(outfile))


if __name__ == "__main__":
	args = parser.parse_args()
	verify_args()
	auto_classify()
