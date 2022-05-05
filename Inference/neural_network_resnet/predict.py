from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from keras.models import load_model
import numpy as np
import time
import os
from os.path import join
from config import INPUT_DIR, OUTPUT_DIR, INPUT_SHAPE, LOAD_MODEL, CLASSES

def load_image(img_path):
  img = image.load_img(img_path, target_size=INPUT_SHAPE)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  return x


def decode_predictions(prediction):
  prediction_decoded = prediction[0]
  data = {}
  for index, cl in enumerate(CLASSES):
    data[cl] = prediction_decoded[index]
  return data


def load_validation_data():
  data = []
  classes = os.listdir(INPUT_DIR)

  for cl in classes:
    validation_class_dir = join(OUTPUT_DIR, 'validation', cl)
    validation_class_files = os.listdir(validation_class_dir)
    validation_class_files.sort()
    validation_class_files_loaded = [load_image(join(validation_class_dir, image)) for image in validation_class_files]
    data.append({
      'class': cl,
      'images_loaded': validation_class_files_loaded,
      'images_path': validation_class_files,
    })
  return data

def predict_images(model, images):
  predictions = [model.predict(image) for image in images]
  return [decode_predictions(pred) for pred in predictions]

def main():

  # load model
  model = load_model(LOAD_MODEL)
  # summarize model.
  # model.summary()

  validation_data = load_validation_data()

  for data in validation_data:
    print(f"------Should be: {data['class']}------")
    start = time.time()
    predictions = predict_images(model, data['images_loaded'])
    end = time.time()
    for index in range(len(data['images_path'])):
      print('Image:', data['images_path'][index])
      print('\tPrediction:', predictions[index])
    print('elapsed time:', end - start)

if __name__ == '__main__':
  main()
