# https://towardsdatascience.com/an-in-depth-efficientnet-tutorial-using-tensorflow-how-to-use-efficientnet-on-a-custom-dataset-1cab0997f65c
# https://keras.io/examples/vision/image_classification_efficientnet_fine_tuning/
# https://machinelearningmastery.com/save-load-keras-deep-learning-models/

import tensorflow as tf
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras import Sequential
from tensorflow.keras import layers
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import image_dataset_from_directory
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from config import CLASSES, BATCH_SIZE, EPOCHS, INPUT_SHAPE, INPUT_DIR, OUTPUT_DIR, LEARNING_RATE, ACTIVATION

def plot_hist(hist, model):
    plt.plot(hist.history["loss"])
    plt.plot(hist.history["val_loss"])
    plt.title("model loss")
    plt.ylabel("loss")
    plt.xlabel("epoch")
    plt.legend(["train", "validation"], loc="upper left")
    # plt.show()
    plt.savefig(os.path.join('models', f"{model}_LOSS.jpg"))

    plt.cla()

    plt.plot(hist.history["accuracy"])
    plt.plot(hist.history["val_accuracy"])
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.legend(["train", "validation"], loc="upper left")
    # plt.show()
    plt.savefig(os.path.join('models', f"{model}_ACC.jpg"))

def get_name_index(prefix):
  found = False
  index = 0
  while not found:
    if not os.path.exists(f"{prefix}-{index}.hdf5"):
      found = True
    else:
      index += 1
  return index

def main():
  train_ds = image_dataset_from_directory(
    os.path.join(OUTPUT_DIR, 'train'),
    image_size=INPUT_SHAPE,
    labels="inferred",
    label_mode="categorical",
    class_names=CLASSES,
    batch_size=BATCH_SIZE,
    shuffle=True,
  ) # 80%

  test_ds = image_dataset_from_directory(
    os.path.join(OUTPUT_DIR, 'test'),
    image_size=INPUT_SHAPE,
    labels="inferred",
    label_mode="categorical",
    class_names=CLASSES,
    batch_size=BATCH_SIZE,
    shuffle=True,
  ) 

  # imgaug
  # run aug before running code
  img_augmentation = Sequential([
      layers.RandomRotation(factor=0.5),
      layers.RandomTranslation(height_factor=0.1, width_factor=0.1),
      layers.RandomFlip(),
      layers.RandomContrast(factor=0.1), # check value
      # blur
      # noise (gaussian, salt and pepper)
    ],
    name='img_augmentation',
  )

  inputs = layers.Input(shape=(INPUT_SHAPE[0], INPUT_SHAPE[1], 3))
  x = img_augmentation(inputs)
  model = ResNet50V2(weights="imagenet", include_top=False, input_tensor=x)
  model.trainable = False

  # Rebuild top
  x = layers.GlobalAveragePooling2D(name="avg_pool")(model.output)
  x = layers.BatchNormalization()(x)

  top_dropout_rate = 0.2
  x = layers.Dropout(top_dropout_rate, name="top_dropout")(x)
  outputs = layers.Dense(len(CLASSES), activation=ACTIVATION, name="pred")(x)

  # Compile
  model = tf.keras.Model(inputs, outputs, name="ResNetV2")
  # optimizer = tf.keras.optimizers.Adam(learning_rate=0.1)
  optimizer = tf.keras.optimizers.SGD(learning_rate=LEARNING_RATE)
  model.compile(
    optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"]
  )


  prefix_name = f"resnetV2-E{EPOCHS}-{len(CLASSES)}C"
  model_name = os.path.join('models', f"{prefix_name}-{get_name_index(prefix_name)}.hdf5")
  checkpoint = ModelCheckpoint(
    model_name,
    monitor='accuracy',
    verbose=1,
    save_best_only=True,
    mode='auto',
    period=1)

  history = model.fit_generator(
    train_ds,
    # steps_per_epoch=len(train_generator.filepaths) // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=test_ds,
    # validation_steps=len(test_generator.filepaths) // BATCH_SIZE,
    verbose=1,
    use_multiprocessing=True,
    workers=4,
    callbacks=[checkpoint],
  )

  plot_hist(history, f"{prefix_name}-{get_name_index(prefix_name)}")

if __name__ == '__main__':
  main()

