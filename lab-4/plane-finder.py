import os

import matplotlib.pyplot as plt
from typing import *
import numpy as np
from scipy.ndimage import *
from skimage import filters
import skimage.color as skic
from skimage.measure import *
from skimage.morphology import *
from skimage.util import *

# region [Typing]
Image = np.ndarray
T = TypeVar('T')
# endregion
# region [Utils]
def foreach(iterable: Iterable[T], fn: Callable[[T], None]):
  [*map(lambda x: fn(*x), iterable)]

def dynamic(**kwargs) -> object:
  return type('dynamic', (), kwargs)
# endregion
# region [Filesystem]
planes_directory: str = 'resources/images/planes/'
output_directory: str = 'outputs/images/planes/'
def image_from(imagename: str, extension: str = 'jpg') -> Image:
  return plt.imread(f"{planes_directory}/{imagename}.{extension}")

def save_to(path: str, image: Image, extension: str = 'jpg', **kwargs):
  plt.imsave(f"{output_directory}/{path}.{extension}", image, **kwargs)

def show(image: Image, **kwargs):
  plt.imshow(image, **kwargs)
  plt.waitforbuttonpress(0.01)
# endregion
# region [Data]
planenames = [f'samolot{i:02}' for i in range(21)]
images = list(map(image_from, planenames))
planes = dict(zip(planenames, images))
# endregion

def as_gray(image: Image) -> Image:
  return 1 - skic.rgb2gray(image)

def dilate(image: Image):
  dilation_seed = np.copy(image)
  dilation_seed[1:-1, 1:-1] = image.min()
  return reconstruction(dilation_seed, mask=image, method='dilation')

def perform_magic(image: Image):
  def create_contoured_image(closed) -> Image:
    def remove_ticks(axes: plt.Axes):
      axes.set_xticks([])
      axes.set_yticks([])

    data: Tuple[plt.Figure, plt.Axes] = plt.subplots()
    (figure, axes) = data

    axes.imshow(image)
    mask = remove_small_holes(closed > threshold, connectivity=2)

    for props in regionprops(labels := label(mask), image):
      contour = find_contours(labels == props.label, threshold)[0]
      if len(contour) < 300: continue
      axes.plot(*reversed(contour.T), linewidth=2)
      axes.plot(*reversed(props.centroid), 'wo', markersize=8)
    remove_ticks(axes)

    figure.savefig('temp.png')
    figure.clear()
    closed = plt.imread('temp.png')
    os.remove('temp.png')
    return closed[:, :, :3]

  grayscale = filters.median(as_gray(image), disk(6))
  dilation = dilate(grayscale)
  dilated = grayscale - dilation
  closed = closing(area_closing(1 - np.power(1 - dilated, 3), 2000), disk(14))

  threshold = filters.threshold_otsu(closed)
  contoured = create_contoured_image(closed)

  return dynamic(
    original=image,
    grayscale=grayscale,
    dilation=dilation,
    dilated=dilated,
    closed=closed,
    threshold=threshold,
    contoured=contoured
  )

def pm(nr): return perform_magic(planes[f"samolot{nr:02}"])

processed_planes = list(map(lambda x: x.contoured, map(perform_magic, images)))
foreach(zip(planenames, processed_planes), save_to)

save_to('collage', montage(processed_planes, multichannel=True))
