import sys
import os

for directory_piece in ["generated", "tests"]:
    sys.path.append(os.path.join(os.path.dirname(__file__), directory_piece))
