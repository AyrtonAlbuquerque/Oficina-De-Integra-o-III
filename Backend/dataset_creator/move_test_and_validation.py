import os
import random
from os import path
import math

INPUT_DIR = '/media/oficinas3/recycler_grayscale_dataset/'
OUTPUT_DIR = '/media/oficinas3/test_temp_dir'
PERCENTAGE_VALID = 0.1
random.seed(10)


if __name__ == '__main__':
    classes = os.listdir(INPUT_DIR)
    images_len = [len(os.listdir(path.join(INPUT_DIR, cl))) for cl in classes]
    cl_with_least_images = min(images_len)
    for cl in classes:
        images = os.listdir(path.join(INPUT_DIR, cl))
        
        images_taken = (len(images) - cl_with_least_images) + math.floor(cl_with_least_images * PERCENTAGE_VALID)
        print(f'{cl} images: {len(images)}')
        validation_sample = random.sample(
          range(len(images)),
          images_taken)
        print('validation_sample:', len(validation_sample), validation_sample[:5])

        class_input_dir = path.join(INPUT_DIR, cl)

        class_validation_dir = path.join(OUTPUT_DIR, 'validation', cl)
        os.makedirs(class_validation_dir, exist_ok=True)
        print('\tvalidation', len(validation_sample), len(validation_sample) / len(images))
        for validation_image_index in validation_sample:
          image_name = images[validation_image_index]
          os.rename(
            path.join(class_input_dir, image_name),
            path.join(class_validation_dir, image_name))
