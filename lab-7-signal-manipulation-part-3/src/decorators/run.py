from typing import Callable

def run(should_run: bool = True) -> Callable:
  def run(fn: Callable[[], None]):
    fn()
  return run if should_run else lambda x: ()
