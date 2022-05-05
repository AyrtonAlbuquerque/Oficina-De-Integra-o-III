
INPUT_DIR = './dataset/Classes' # dir with all images/classes
OUTPUT_DIR = './dataset/Classes_split' # dir to put splittled images/classes
CLASSES = ['metal_can', 'paper_ball', 'plastic_bottle']
PERCENTAGE_TEST = 0.15 # percentage of images that will be used for testing
PERCENTAGE_VALIDATE = 0.05 # percentage of images that will be used for validation
SHUFFLE = True # if dataset will be shuffled at the splitting process
INPUT_SHAPE = (224, 224) # shape of the image (dependent on network)
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.01 # https://machinelearningmastery.com/understand-the-dynamics-of-learning-rate-on-deep-learning-neural-networks/
ACTIVATION = "sigmoid" # https://keras.io/api/layers/activations/
LOAD_MODEL='./models/resnetV2-E10-3C-0.hdf5' # model to load on prediction