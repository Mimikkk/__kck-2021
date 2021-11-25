from typing import *

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy
import numpy as np
from matplotlib import colors

# region [Typing]
Color = Tuple[float, float, float]
RgbColor = Color
HsvColor = Color
# endregion

# region [Matplotlib Customization]
rc('legend', fontsize=10)
# endregion

# region [Utils]
def hsv2rgb(color: HsvColor) -> RgbColor:
  (h, s, v) = color

  i = int(h * 6)
  f = (h * 6) - i
  p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
  i %= 6
  if i == 0: return (v, t, p)
  if i == 1: return (q, v, p)
  if i == 2: return (p, v, t)
  if i == 3: return (p, q, v)
  if i == 4: return (t, p, v)
  if i == 5: return (v, p, q)

def foreach(iterable: Iterable, function: Callable):
  [*map(lambda x: function(*x), iterable)]
# endregion

coloring: Dict[str, RgbColor] = {
  'white': (1, 1, 1),
  'black': (0, 0, 0),
  'red': (1, 0, 0),
  'green': (0, 1, 0),
  'blue': (0, 0, 1),
  'teal': (0, 1, 1),
  'magenta': (1, 0, 1),
  'yellow': (1, 1, 0),
}

class RgbGradient(object):
  @staticmethod
  def bw(value) -> RgbColor:
    return RgbGradient.gradient(value, list(map(coloring.__getitem__, ('black', 'white'))))

  @staticmethod
  def gbr_partial(value) -> RgbColor:
    return RgbGradient.gradient(value, list(map(coloring.__getitem__, ('green', 'blue', 'red'))))

  @staticmethod
  def gbr_full(value) -> RgbColor:
    spectrum = list(map(coloring.__getitem__, ('green', 'teal', 'blue', 'magenta', 'red')))
    return RgbGradient.gradient(value, spectrum)

  @staticmethod
  def custom(value) -> RgbColor:
    spectrum = list(map(coloring.__getitem__, ('white', 'magenta', 'blue', 'teal', 'green', 'yellow', 'red', 'black')))
    return RgbGradient.gradient(value, spectrum)

  @classmethod
  def gradient(cls, value, colors: Tuple[RgbColor, ...]) -> RgbColor:
    size = len(colors)
    for i in range(size - 1):
      min = (size - i - 2) / (size - 1)
      if (value > min):
        max = (size - i - 1) / (size - 1)
        (first, second) = colors[size - i - 2:size - i]
        return cls.interpolate_colors(first, second, weight=np.interp(value, (min, max), (0, 1)))

  @staticmethod
  def interpolate(first: float, second: float, fraction: float) -> RgbColor:
    return (second - first) * fraction + first

  @classmethod
  def interpolate_colors(cls, first: RgbColor, second: RgbColor, weight: float) -> RgbColor:
    (r1, g1, b1) = first
    (r2, g2, b2) = second
    return (cls.interpolate(r1, r2, weight), cls.interpolate(g1, g2, weight), cls.interpolate(b1, b2, weight))

class HsvGradient(object):
  @staticmethod
  def bw(value: float) -> HsvColor:
    return hsv2rgb((0, 0, value))

  @staticmethod
  def gbr(value: float) -> HsvColor:
    return hsv2rgb((np.interp(value, (0, 1), (1 / 3, 1)), 1, 1))

  @staticmethod
  def unknown(value: float) -> HsvColor:
    return hsv2rgb((np.interp(1 - value, (0, 1), (0, 1 / 4)), 0.5, 1))

  @staticmethod
  def custom(value: float) -> HsvColor:
    return hsv2rgb((value, 1 - value, 1))

def plot_gradients(gradients: Dict[str, Callable[[Color], Color]]):
  def assign_name(axes: plt.Axes, name: str):
    (_, x2, *_) = axes.get_position().bounds
    figure.text(0, x2 + .05, name, va='center', ha='left', fontsize=10)

  def create_gradient_image(gradient_fn: Callable[[float], Color]) -> np.ndarray:
    def assign_color(index: int, value: float): gradient[:, index] = gradient_fn(value)

    gradient = np.zeros((2, 1024, 3))
    foreach(enumerate(np.linspace(0, 1, 1024)), assign_color)
    return gradient

  def plot_gradient(axes: plt.Axes, gradient: np.ndarray):
    image = axes.imshow(gradient, aspect='auto')
    image.set_extent([0, 1, 0, 1])
    axes.yaxis.set_visible(False)

  column_width_pt = 400
  pt_per_inch = 72
  size = column_width_pt / pt_per_inch

  (figure, axes) = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
  figure.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

  foreach(zip(axes, map(create_gradient_image, gradients.values())), plot_gradient)
  foreach(zip(axes, list(gradients)), assign_name)

  figure.savefig('gradients.pdf')

plot_gradients({
  'RGB_BW': RgbGradient.bw,
  'RGB_GBR': RgbGradient.gbr_partial,
  'RGB_GBR_FULL': RgbGradient.gbr_full,
  'RGB_WB_CUSTOM': RgbGradient.custom,
  'HSV_BW': HsvGradient.bw,
  'HSV_GBR': HsvGradient.gbr,
  'HSV_UNKNOWN': HsvGradient.unknown,
  'HSV_CUSTOM': HsvGradient.custom,
})
