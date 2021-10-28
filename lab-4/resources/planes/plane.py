import os


for i in range(21):
  os.rename(f"plane{i}.jpg", f"samolot{i:02}.jpg")
