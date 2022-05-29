from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from keras.models import load_model
import numpy as np
import time
import os
from os.path import join
from config import OUTPUT_DIR, INPUT_SHAPE, LOAD_MODEL, CLASSES

def load_image(img_path):
  img = image.load_img(img_path, target_size=INPUT_SHAPE)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  return x


def decode_predictions(predictions):
  # print('prediction', predictions)
  max_confidence_prediction = max(predictions)
  # print('max_confidence_prediction', max_confidence_prediction)
  if max_confidence_prediction > 0.75:
    return np.where(predictions == max_confidence_prediction)[0][0].item()
  return -1

  prediction_decoded = prediction[0]
  data = {}
  for index, cl in enumerate(CLASSES):
    data[cl] = prediction_decoded[index]
  return data


def load_validation_data():
  data = []

  for cl in CLASSES:
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
  return [decode_predictions(pred[0]) for pred in predictions]

def main():

  # load model
  model = load_model(LOAD_MODEL)
  # summarize model.
  # model.summary()

  validation_data = load_validation_data()

  all = 0
  correct_all = 0
  for data in validation_data:
    print(f"------Should be: {data['class']}------")
    should_be = CLASSES.index(data['class'])
    start = time.time()
    predictions = predict_images(model, data['images_loaded'])
    correct = len([p for p in predictions if p == should_be])
    all += len(predictions)
    correct_all += correct
    print(f"Class: {data['class']} - images: {len(predictions)} - correct {correct} {correct*100/len(predictions):.2f}")
    end = time.time()
    #for index in range(len(data['images_path'])):
    #  print('Image:', data['images_path'][index])
    #  print('\tPrediction:', predictions[index])
    print('elapsed time:', end - start)
  print(f"Result - images: {all} - correct {correct_all} {correct_all*100/all:.2f}")

if __name__ == '__main__':
  main()
