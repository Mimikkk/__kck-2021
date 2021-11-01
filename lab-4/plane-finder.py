import matplotlib.pyplot as plt
from typing import *
import numpy as np
import skimage as ski
import skimage.measure as skim

def foreach(iterable: Iterable, fn: Callable): [*map(lambda x: fn(*x), iterable)]

Image = np.ndarray
planes_directory: str = 'resources/images/planes/'
output_directory: str = 'outputs/images/planes/'
def image_from(imagename: str, extension: str = 'jpg') -> Image:
  return plt.imread(f"{planes_directory}/{imagename}.{extension}")

def find_plane(image: Image) -> Image:

  pass

def save_to(path: str, image: Image, extension: str = 'jpg'):
  plt.imsave(f"{output_directory}/{path}.{extension}", image)

def show(image: Image):
  plt.imshow(image)
  plt.waitforbuttonpress()

planes = [f'samolot{i:02}' for i in range(21)]

