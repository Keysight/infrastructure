import os
import sys

sys.path.extend(
    [
        os.path.join(os.path.dirname(__file__), ".."),
        os.path.join(os.path.dirname(__file__), "../generated"),
    ]
)
