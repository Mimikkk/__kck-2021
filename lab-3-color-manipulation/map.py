import matplotlib.pyplot as plt
from typing import *
import numpy as np

# region [Classes]
class Texture(object):
  def __init__(self, points: list, distance: float = None):
    self.points = np.array(points)
    self.min = self.points.min(initial=1)
    self.max = self.points.max(initial=0)
    (self.width, self.height, *_) = self.points.shape
    self.distance = distance or 1

# endregion

# region [Typing]
Color = Tuple[float, float, float]
RgbColor = Color
HsvColor = Color

HeightMap = Texture
ShadeMap = Texture
TerrainMap = Texture
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

def scale(value: float,
          fn: Callable[[float], float],
          range1: Tuple[float, float],
          range2: Tuple[float, float]) -> float:
  return np.interp(fn(np.interp(value, range1, (0, 1))), (0, 1), range2)
# endregion

def load_map(filepath: str) -> Optional[HeightMap]:
  with open(filepath, 'r') as file:
    (_, height, distance) = map(int, file.readline().split())

    points = np.array([np.array([*map(float, file.readline().split())]) for _ in range(height)])
    return Texture(points / 255, distance)

#Slightly modified source: https://www.neonscience.org/resources/learning-hub/tutorials/create-hillshade-py
def hillshade(height_map: HeightMap, azimuth: float, angle_altitude: float) -> ShadeMap:
  def shade_in():
    return np.sin(angle_altitude * np.pi / 180) \
           * np.sin(slope) \
           + np.cos(angle_altitude * np.pi / 180) \
           * np.cos(slope) \
           * -np.cos((-azimuth * np.pi / 180) - aspect)

  (dx, dy) = np.gradient(height_map.points, height_map.distance / 100)
  slope = np.pi / 2 - np.arctan(np.sqrt(np.square(dx) + np.square(dy)))
  aspect = np.arctan2(-dx, dy)
  return Texture(shade_in())

def gradient(height_map: HeightMap, shade_map: ShadeMap) -> TerrainMap:
  def terrain_gradient(height: float, shade: float) -> RgbColor:
    return hsv2rgb((5 / 9 - 5 / 9 * height, 1 - 0.8 * shade, 0.5 + 0.5 * shade))

  def ease_in(x: float) -> float:
    return 1 - np.power(-2 * x + 2, 1.76) / 2

  gradient: np.ndarray = np.zeros((*shade_map.points.shape, 3))
  for i in range(shade_map.height):
    for j in range(shade_map.width):
      gradient[i, j] = \
        terrain_gradient(
          scale(height_map.points[i, j], ease_in, (height_map.min, height_map.max), (0, 1)),
          scale(shade_map.points[i, j], ease_in, (shade_map.min, shade_map.max), (0, 1))
        )
  return Texture(gradient)

height_map = load_map('resources/height_maps/map.dem')
shade_map = hillshade(height_map, 70, 60)
terrain_map = gradient(height_map, shade_map)

plt.imsave('maps/height.png', height_map.points, cmap='Greys')
plt.imsave('maps/shaded.png', shade_map.points, cmap='Greys')
plt.imsave('maps/terrain.png', terrain_map.points)
