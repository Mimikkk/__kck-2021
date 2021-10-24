from typing import *

# region [Typing]
Color = Tuple[float, float, float]
RgbColor = Color
HsvColor = Color
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

class TerrainMap(object):
  def __init__(self, width: int, height: int, distance: float, points: list):
    self.width = width
    self.height = height
    self.distance = distance
    self.points = points[:]

def load_map(filepath: str) -> Optional[TerrainMap]:
  with open('map.dem', 'r') as file:
    (width, height, distance) = map(int, file.readline().split())
    points = [list(map(float, file.readline().split())) for _ in range(height)]
    return TerrainMap(width, height, distance, points)
