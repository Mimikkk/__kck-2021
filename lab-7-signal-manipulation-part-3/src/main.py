from __future__ import annotations

from constants import VoiceCount, ModelName
from decorators import run
from model import Model
import voice_loader

@run(True)
def main():
  voices = voice_loader.shuffled(VoiceCount)
  model = Model.complied(ModelName)


  @run(True)
  def train():
    pass

  model.load(ModelName)

  @run(True)
  def voice_presenter():
    pass

  @run(True)
  def webcam():
    def window():
      pass

