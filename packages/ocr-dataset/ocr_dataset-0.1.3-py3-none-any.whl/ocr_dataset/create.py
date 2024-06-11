from typing import Sequence
import os
import fs
from .dataset import Meta

def create_tar(
  base_path: str,
  samples: Sequence[tuple[bytes, str]], *,
  images_name: str = 'images',
  labels_name: str = 'labels',
  images_ext: str = 'jpg',
):
  os.makedirs(base_path, exist_ok=True)
  meta = Meta.new_tar(len(samples), images=images_name, labels=labels_name)
  with open(f'{base_path}/meta.json', 'w') as f:
    f.write(meta.model_dump_json(indent=2))

  imgs, labs = zip(*samples)
  
  num_digits = len(str(len(samples)))
  files = [(f'{i:0{num_digits}}.{images_ext}', img) for i, img in enumerate(imgs)]
  fs.create_tarfile(files, f'{base_path}/{images_name}.tar')

  with open(f'{base_path}/{labels_name}.txt', 'w') as f:
    f.write('\n'.join(labs) + '\n')