import os, json, re
import numpy as np
import pandas as pd
import pickle
from glob import glob
from PIL import Image
from matplotlib import pyplot as plt
from shutil import copyfile


def save_array(fname, arr):
    c=bcolz.carray(arr, rootdir=fname, mode='w')
    c.flush()
def load_array(fname):
    return bcolz.open(fname)[:]

def dump(obj, fname): pickle.dump(obj, open(fname, 'wb'))
def load(fname): return pickle.load(open(fname, 'rb'))

# find ./wwend_all_books -type f -name "*.jpg" -exec cp {} ../train/books/train/ \; -print