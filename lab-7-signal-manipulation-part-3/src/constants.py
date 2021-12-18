from os import getcwd
from os.path import join

Paths: dict[str, str] = {
  "voices": join(getcwd(), 'resources', 'voices'),
  "models": join(getcwd(), 'resources', 'models'),
}

VoiceCount: int = 91
ModelName: str = 'Wino'
