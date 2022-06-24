import os
from os import path

INPUT_DIR = '/media/oficinas3/annotated_dataset/juice_box'
OUTPUT_DIR = '/media/oficinas3/annotated_dataset/juice_box'
PREFIX = 'juice_box_out_'

def seq(n, size):
  n_str = str(n)
  return ('0' * size)[:size - len(n_str)] + n_str

files = os.listdir(INPUT_DIR)
for index, file in enumerate(files):
  basename, ext = path.splitext(file)
  src = path.join(INPUT_DIR, file)
  dst = path.join(OUTPUT_DIR, f'{PREFIX}{seq(index, 4)}{ext}')
  os.rename(src, dst)