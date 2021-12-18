from __future__ import annotations

from dataclasses import dataclass
from os.path import join
from typing import Any

from keras import Sequential
from keras.backend import binary_crossentropy
from keras.callbacks import Callback, ModelCheckpoint, BaseLogger, History, EarlyStopping
from keras.engine.input_layer import InputLayer
from keras.layers import Dense
from keras.optimizer_v2 import adam
from numpy.typing import NDArray

from constants import Paths

@dataclass
class Model(object):
  _handle: Sequential
  name: str

  @classmethod
  def uncompiled(cls, modelname: str) -> Model:
    return Model(Sequential([
      InputLayer((1, 1, 1)),
      Dense(2, activation='sigmoid')
    ]), modelname)

  @classmethod
  def complied(cls, modelname: str) -> Model:
    model = cls.uncompiled(modelname)
    model._handle.compile(loss=binary_crossentropy, optimizer=adam, metrics=['accuracy'])
    return model

  @classmethod
  def load(cls, modelname: str) -> Model:
    model = cls.complied(modelname)
    model._handle.load_weights(join(Paths['models'], f"{modelname}.h5"))
    return model

  def predict(self, item: Any) -> list[int]:
    return self._handle.predict(item)[0]

  def save(self):
    self._handle.save(join(Paths['models'], f"{self.name}.h5"))

  def callbacks(self) -> list[Callback]:
    return [
      ModelCheckpoint(filepath=f"{Paths['models']}/best_{self.name}.h5", save_best_only=True),
      EarlyStopping(monitor='val_loss', patience=5, mode='auto'),
      BaseLogger(),
    ]

  def train(self, images: NDArray, labels: NDArray, epochs: int):
    return self._handle.fit(
      images,
      labels,
      epochs=epochs,
      callbacks=self.callbacks()
    )

  def summary(self):
    self._handle.summary()
