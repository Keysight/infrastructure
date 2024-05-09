"""Container class for various infrastructure utility methods
"""
from typing import List, Tuple

class Utilities:
    def get_indexes(c1, c2) -> List[Tuple[str, List[int]]]:
        max = c1 if c1.count >= c2.count else c2
        min = c2 if max.name == c1.name else c1
        step = int(max.count / min.count)
        min_idxs = []
        for idx in range(min.count):
            min_idxs.extend([idx] * step)
        return [[max.name, range(max.count)], [min.name, min_idxs]]

    def repeat_package(package, component, max_count):
        """Returns a list"""
        indexes = []
        while len(indexes) < max_count * package:
            for i in range(package):
                indexes.extend(itertools.repeat(i, min(max_count, component)))
        return indexes

    def list_package(package, component, max_count):
        """Returns a list"""
        indexes = []
        while len(indexes) < max_count * package:
            for i in range(package):
                indexes.extend(itertools.repeat(i, package))
            indexes.extend(reversed(indexes))
        return indexes

    def cycle_component(component, max_count):
        """Returns a list"""
        return itertools.cycle(range(0, min(max_count, component)))

    def get_adjacency_indexes(p1, c1, p2, c2, max_count, mesh) -> dict:
        """Returns a dict of param to name and indexes
        ie "p1": {name: "p1", indexes: []}
        """
        indexes = {
            "p1": {"name": p1.name, "indexes": None},
            "c1": {"name": c1.name, "indexes": None},
            "p2": {"name": p2.name, "indexes": None},
            "c2": {"name": c2.name, "indexes": None},
        }
        indexes["p1"]["indexes"] = Utilities.repeat_package(
            p1.count, c1.count, max_count
        )
        indexes["c1"]["indexes"] = Utilities.cycle_component(c1.count, max_count)
        if mesh is True:
            indexes["p2"]["indexes"] = Utilities.list_package(
                p2.count, c2.count, max_count
            )
        else:
            indexes["p2"]["indexes"] = Utilities.repeat_package(
                p2.count, c2.count, max_count
            )
        indexes["c2"]["indexes"] = Utilities.cycle_component(c2.count, max_count)
        return indexes
