from pyboy import PyBoy
import os

def _game_files_root() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "ROMs/Pokemon_Red/Pokemon_Red.gb")

root = _game_files_root()

pyboy = PyBoy(root)
while not pyboy.tick():
    pass

pyboy.stop()