from os import listdir
from random import shuffle, sample

from constants import Paths
from structures import Voice

def load(count: int) -> list[Voice]:
  paths = listdir(Paths['voices'])
  shuffle(paths)

  print("Loading voices...")
  return list(map(Voice.from_path, paths[:count]))

def shuffled(count: int) -> list[Voice]:
  return sample(load(count), count)
