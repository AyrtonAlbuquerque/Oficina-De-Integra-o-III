from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from keras.models import load_model
import numpy as np
import time
import os
from os.path import join
from src.config import MODEL_PATH, PREDICTION_THRESHOLD, INPUT_SHAPE


def load_image(img_path):
  img = image.load_img(img_path, target_size=INPUT_SHAPE)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  return x

def decode_predictions(predictions):
  print('prediction', predictions)
  max_confidence_prediction = max(predictions)
  print('max_confidence_prediction', max_confidence_prediction)
  if max_confidence_prediction > PREDICTION_THRESHOLD:
    return np.where(predictions == max_confidence_prediction)[0][0].item()
  return -1

  for index, pred in enumerate(prediction):
    if pred >= PREDICTION_THRESHOLD:
      possible.append({
        'index': index,
        'confidence': pred
      })
  if len(possible):
    return max(possible, key = lambda k: square['confidence'])['index']


# load model
model = load_model(MODEL_PATH)

def classify(image_path):
  print('image_path', image_path)
  image = load_image(image_path)
  prediction = model.predict(image)
  print('prediction', prediction)
  classification = decode_predictions(prediction[0])
  print('classification', classification)
  return classification