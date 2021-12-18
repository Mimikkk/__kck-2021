from __future__ import annotations
from dataclasses import dataclass

from constants import Paths
from scipy.io.wavfile import read

@dataclass
class Voice(object):
  sample_rate: int
  sound: list[float]
  label: str

  @classmethod
  def from_path(cls, filepath: str) -> Voice:
    (sample_rate, sound) = read(f"{Paths['voices']}/{filepath}")
    label = 'Male' if 'M' in filepath else 'Female'
    return cls(sample_rate, sound, label)
