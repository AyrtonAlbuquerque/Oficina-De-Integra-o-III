PORT = 8081
JWT_KEY = 'secret_key'
STORAGE_PATH = '/media/oficinas3/backend_data'
MODEL_PATH = '/home/ian/Documents/code/Oficina-De-Integra-o-III/Inference/neural_network_resnet/models/resnetV2-E10-2C-0.hdf5'
CLASSES = ['metal_can', 'plastic_bottle', 'paper_ball', 'plastic_cup', 'juice_box', 'chips_bag']
LOAD_TEST_DATA = True
INPUT_SHAPE = (224, 224) # shape of the image (dependent on network)
PREDICTION_THRESHOLD = 0.7 # if a prediction is more than this level of confidence, it will be considered