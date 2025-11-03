import sys
print("Python version:", sys.version, flush=True)

print("Importing os...", flush=True)
import os

print("Setting Keras backend...", flush=True)
os.environ['KERAS_BACKEND'] = 'jax'

print("Importing keras...", flush=True)
import keras

print("Keras version:", keras.__version__, flush=True)
print("Backend:", keras.backend.backend(), flush=True)

print("Importing other modules...", flush=True)
from PIL import Image
import numpy as np
import glob

print("All imports successful!", flush=True)

