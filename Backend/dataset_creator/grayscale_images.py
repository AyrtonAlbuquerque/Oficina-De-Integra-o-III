import os
import os.path as path
from PIL import Image, ImageOps

INPUT_DIR = '/media/oficinas3/recycler_annotated_dataset/'
OUTPUT_DIR = '/media/oficinas3/recycler_grayscale_dataset/'


def main():
  classes = os.listdir(INPUT_DIR)

  for cl in classes:
    os.makedirs(path.join(OUTPUT_DIR, cl), exist_ok=True)
    cl_dir = path.join(INPUT_DIR, cl)
    output_cl_dir = path.join(OUTPUT_DIR, cl)
    cl_dir_images = os.listdir(cl_dir)
    for image in cl_dir_images:
      image_path = path.join(cl_dir, image)
      print('Grayscaling image', image_path)
      og_image = Image.open(image_path)
      gray_image = ImageOps.grayscale(og_image)
      gray_image.save(path.join(output_cl_dir, image))

if __name__ == '__main__':
  main()
