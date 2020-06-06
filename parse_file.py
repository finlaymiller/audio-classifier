import numpy as np
from scipy.io import wavfile
import tensorflow as tf

def process_file(wav_file):
	"""Reads input wav file and prints predictions to terminal

	Args:
		wav_file: file to be classified. Must be 16-bit PCM.

	Returns:
		None.
	"""
	sr, data = wavfile.read(wav_file)
	if data.dtype != np.int16:
		raise TypeError('Bad sample type encountered when reading file \'%s\'' % wav_file)

	# local import to reduce start-up time
	from audio.processor import WavProcessor, format_predictions

	with WavProcessor() as proc:
		predictions = proc.get_predictions(sr, data)

	print("\n------------------------------------------------------------------------------------")
	print(format_predictions(predictions))
	print("------------------------------------------------------------------------------------\n")

	return sr, data.shape, format_predictions(predictions)