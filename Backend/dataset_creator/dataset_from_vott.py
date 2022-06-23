import json
import os
import os.path as path
from PIL import Image
from urllib.parse import unquote

VOTT_OUTPUT = '/media/oficinas3/recycler_annotation_project'
OUTPUT_DIR = '/media/oficinas3/temp'

def create_dir(path):
  if not os.path.exists(path):
    os.makedirs(path)

def sequential(n, size):
  n_str = str(n)
  return ('0'*size)[:size-len(n_str)] + n_str

def main():
  files = [file for file in os.listdir(VOTT_OUTPUT) if file.endswith('-asset.json')]
  assets = []
  for file in files:
    with open(path.join(VOTT_OUTPUT, file)) as fp:
      def parse_path(path, name):
        return path.replace('file:', '').replace(name, '')
      def parse_region(region):
        return {
          'class_name': region['tags'][0],
          'boundingBox': (
            region['boundingBox']['left'], # left
            region['boundingBox']['top'], # top
            region['boundingBox']['left'] + region['boundingBox']['width'], # right
            region['boundingBox']['top'] + region['boundingBox']['height'], # bottom
          ),
        }
      data = json.load(fp)
      parsed = {
        'name': unquote(data['asset']['name']),
        'path': unquote(parse_path(data['asset']['path'], data['asset']['name'])),
        'boxes': [parse_region(region) for region in data['regions']]
      }
      assets.append(parsed)

  # print(json.dumps(assets[5:10], indent=2))

  class_name_index = {}
  for asset in assets:
    image_path = path.join(asset['path'], asset['name'])
    image = Image.open(image_path)
    for box in asset['boxes']:
      class_name = box['class_name']
      cropped = image.crop(box['boundingBox'])
      class_path = path.join(OUTPUT_DIR, class_name)
      if not class_name in class_name_index:
        class_name_index[class_name] = 0
        create_dir(class_path)
      index = class_name_index[class_name]
      save_path = path.join(class_path, f"{class_name}_{sequential(index, 4)}.png")
      print('Saving image:', save_path)
      cropped.save(save_path)

      class_name_index[class_name] += 1


      
if __name__ == '__main__':
  main()
