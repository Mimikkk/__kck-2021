import os
import matplotlib.pyplot as plt
from typing import *
import numpy as np
from skimage import filters
import skimage.color as skic
from skimage.measure import find_contours
from skimage.morphology import *

# region [Typing]

Image = np.ndarray
T = TypeVar('T')

# endregion
# region [Utils]
def foreach(iterable: Iterable[T], fn: Callable[[T], None]):
  [*map(lambda x: fn(*x), iterable)]

def flow(*fns: List[Callable[[T], T]]) -> Callable[[Iterable[T]], Iterable[T]]:
  def wrapper(iterable: Iterable[T]):
    for fn in fns: iterable = map(fn, iterable)
    return iterable
  return wrapper

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

def perform_magic(image: Image):
  def create_contoured_image(closed) -> plt.Figure:
    def remove_ticks(axes: plt.Axes):
      axes.set_xticks([])
      axes.set_yticks([])

    data: Tuple[plt.Figure, plt.Axes] = plt.subplots()
    (figure, axes) = data

    for contour in find_contours(closed > 0.2, threshold):
      axes.plot(contour[:, 1], contour[:, 0], linewidth=2)

    remove_ticks(axes)
    figure.savefig('temp.png')
    figure.clear()

    closed = plt.imread('temp.png')
    os.remove('temp.png')
    return closed[:, :, :3]

  grayscale = as_gray(image)
  threshold = filters.threshold_otsu(grayscale)
  # mask = grayscale > threshold
  grayscale = filters.median(grayscale, disk(5))

  dilation_seed = np.copy(grayscale)
  dilation_seed[1:-1, 1:-1] = grayscale.min()
  dilated = reconstruction(dilation_seed, mask=grayscale, method='dilation')
  closed = closing(grayscale - dilated, disk(8))

  return dynamic(
    original=image,
    gray=grayscale,
    dilate=grayscale - dilated,
    dilated=dilated,
    closed=closed,
    contoured=create_contoured_image(np.copy(closed)),
  )

def pm(nr): return perform_magic(planes[f"samolot{nr:02}"])
# processed_planes = list(flow(as_gray, create_contoured_image)(images))
# foreach(zip(planenames, processed_planes), save_to)


# mend mask with dilation
