import os
from os.path import join
import pathlib
import shutil
import random

INPUT_DIR = '/media/oficinas3/recycler_grayscale_augmented_dataset/'
OUTPUT_DIR = '/media/oficinas3/recycler_grayscale_training_dataset/'
PERCENTAGE_TEST = 0.2
SHUFFLE = True

random.seed(10)

def create_dir(path):
  if not os.path.exists(path):
    os.makedirs(path)


def create_dataset():
  train_path = os.path.join(OUTPUT_DIR, 'train')
  print('Creating train path:', train_path)
  create_dir(train_path)

  test_path = os.path.join(OUTPUT_DIR, 'test')
  print('Creating test path:', test_path)
  create_dir(train_path)

  classes = os.listdir(INPUT_DIR)
  print(f'Found {len(classes)} classes')

  for cl in classes:
    print('Copying class:', cl)
    train_class_path = join(train_path, cl)
    test_class_path = join(test_path, cl)

    create_dir(train_class_path)
    create_dir(test_class_path)

    input_dir_class_path = join(INPUT_DIR, cl)
    files = os.listdir(input_dir_class_path)
    print('\tQuantity of files:', len(files))

    if SHUFFLE:
      random.shuffle(files)
  
    test_files_length = int(PERCENTAGE_TEST * len(files))
    test_files = files[:test_files_length]
    train_files = files[test_files_length:]

    print('\tTrain files:', len(train_files))
    print('\tTest files:', len(test_files))

    for file in train_files:
      shutil.copyfile(join(input_dir_class_path, file), join(train_class_path, file))

    for file in test_files:
      shutil.copyfile(join(input_dir_class_path, file), join(test_class_path, file))


def test_prepare_dataset():
  prepare_dataset()

if __name__ == '__main__':
  create_dataset()