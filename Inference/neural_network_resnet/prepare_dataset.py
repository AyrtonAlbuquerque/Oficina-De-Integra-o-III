import os
from os.path import join
import pathlib
import shutil
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import random
from config import INPUT_DIR, OUTPUT_DIR, PERCENTAGE_TEST, PERCENTAGE_VALIDATE, SHUFFLE, CLASSES

def create_dir(path):
  if not os.path.exists(path):
    os.makedirs(path)


def create_dataset(input_dir, output_dir, percentage_test=0.15, percentage_validation=0.05, clean_output=False, shuffle=True):
  if clean_output:
    os.rmdir(output_dir)
    create_dir(output_dir)

  train_path = os.path.join(output_dir, 'train')
  print('Creating train path:', train_path)
  create_dir(train_path)

  test_path = os.path.join(output_dir, 'test')
  print('Creating test path:', test_path)
  create_dir(train_path)

  validation_path = os.path.join(output_dir, 'validation')
  print('Creating validation path:', validation_path)
  create_dir(validation_path)

  classes = CLASSES
  print(f'Found {len(classes)} classes')

  for cl in classes:
    print('Copying class:', cl)
    train_class_path = join(train_path, cl)
    test_class_path = join(test_path, cl)
    validation_class_path = join(validation_path, cl)

    create_dir(train_class_path)
    create_dir(test_class_path)
    create_dir(validation_class_path)

    input_dir_class_path = join(input_dir, cl)
    files = os.listdir(input_dir_class_path)
    print('\tQuantity of files:', len(files))

    if shuffle:
      random.shuffle(files)
  
    test_files_length = int(percentage_test * len(files))
    validation_files_length = int(percentage_validation * len(files))
    test_files = files[:test_files_length]
    validation_files = files[test_files_length:test_files_length + validation_files_length]
    train_files = files[test_files_length + validation_files_length:]

    print('\tTrain files:', len(train_files))
    print('\tTest files:', len(test_files))
    print('\tValidation files:', len(validation_files))

    for file in train_files:
      shutil.copyfile(join(input_dir_class_path, file), join(train_class_path, file))

    for file in test_files:
      shutil.copyfile(join(input_dir_class_path, file), join(test_class_path, file))

    for file in validation_files:
      shutil.copyfile(join(input_dir_class_path, file), join(validation_class_path, file))

def test_prepare_dataset():
  prepare_dataset()

if __name__ == '__main__':
  create_dataset(
    INPUT_DIR,
    OUTPUT_DIR,
    percentage_test=PERCENTAGE_TEST,
    percentage_validation=PERCENTAGE_VALIDATE,
    shuffle=SHUFFLE)