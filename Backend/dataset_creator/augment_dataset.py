import numpy as np
import imgaug
import imgaug.augmenters as iaa
from PIL import Image
from matplotlib import pyplot as plt
import os
from os import path
import math

SAVE_IMAGES = True
AUGMENTATION_SEED = 10
INPUT_DIR = '/media/oficinas3/recycler_grayscale_dataset/'
OUTPUT_DIR = '/media/oficinas3/recycler_grayscale_augmented_dataset/'
IMAGES_QUANTITY = 6
GRAYSCALE = True
# images_quantity = 0

imgaug.seed(AUGMENTATION_SEED)


def seq(n, size):
  n_str = str(n)
  return ('0' * size)[:size - len(n_str)] + n_str

def augment_image(dataset_class, filename):
    basename, ext = path.splitext(filename)
    image = Image.open(path.join(INPUT_DIR, dataset_class, filename))
    image_array = np.array(image)

    images = np.array(
        [image_array for _ in range(IMAGES_QUANTITY)],
        dtype=np.uint8
    )
    seq = iaa.Sequential([
        # iaa.Fliplr(0.5), # horizontal flips
        # Small gaussian blur with random sigma between 0 and 0.5.
        # But we only blur about 50% of all images.
        iaa.Sometimes(
            0.5,
            iaa.GaussianBlur(sigma=(0, 0.5))
        ),
        # For 50% of all images, we sample the noise once per pixel.
        # For the other 50% of all images, we sample the noise per pixel AND
        # channel. This can change the color (not only brightness) of the
        # pixels.
        # iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
        iaa.Sometimes(
            0.25,
            iaa.SaltAndPepper()
        ),
        iaa.Sometimes(
            0.25,
            iaa.contrast.GammaContrast()
        ),
        # Make some images brighter and some darker.
        # In 20% of all cases, we sample the multiplier once per channel,
        # which can end up changing the color of the images.
        # iaa.Multiply((0.8, 1.2), per_channel=0.2),
        # Apply affine transformations to each image.
        iaa.Affine(
            # scale={"x": (0.9, 1.1), "y": (0.9, 1.1)},
            rotate=(-180, 180),
            fit_output=True
        ),
    ], random_order=True) # apply augmenters in random order

    images_aug = seq(images=images)

    if SAVE_IMAGES:
        output_dir = path.join(OUTPUT_DIR, dataset_class)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        for (index, image) in enumerate(images_aug):
            if GRAYSCALE:
                plt.imsave(path.join(output_dir, f'{basename}_{index:02d}.jpg'), image, cmap='gray')
            else:
                plt.imsave(path.join(output_dir, f'{basename}_{index:02d}.jpg'), image)


if __name__ == '__main__':
    classes = os.listdir(INPUT_DIR)
    for cl in classes:
        images = os.listdir(path.join(INPUT_DIR, cl))
        # images_quantity = math.ceil(AMOUNT_IMAGES / len(images))
        print(f'Augmenting class {cl}')
        for image in images:
            # print('Augumenting image:', cl, image)
            augment_image(cl, image)