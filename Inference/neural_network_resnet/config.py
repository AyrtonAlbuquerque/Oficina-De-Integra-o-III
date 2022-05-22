
INPUT_DIR = '/media/oficinas3/augumentated_dataset' # dir with all images/classes
OUTPUT_DIR = '/media/oficinas3/training_dataset' # dir to put splittled images/classes
CLASSES = ['metal_can', 'plastic_bottle', 'paper_ball', 'plastic_cup', 'juice_box', 'chips_bag']
PERCENTAGE_TEST = 0.15 # percentage of images that will be used for testing
PERCENTAGE_VALIDATE = 0.05 # percentage of images that will be used for validation
SHUFFLE = True # if dataset will be shuffled at the splitting process
INPUT_SHAPE = (224, 224) # shape of the image (dependent on network)
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.01 # https://machinelearningmastery.com/understand-the-dynamics-of-learning-rate-on-deep-learning-neural-networks/
ACTIVATION = "sigmoid" # https://keras.io/api/layers/activations/
LOAD_MODEL='./models/resnetV2-E10-2C-0.hdf5' # model to load on prediction
PREDICTION_THRESHOLD = 0.8 # if a prediction is more than this level of confidence, it will be considered