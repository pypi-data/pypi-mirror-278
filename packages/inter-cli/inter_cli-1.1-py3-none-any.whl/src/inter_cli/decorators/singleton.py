from typing import Any


def singleton(cls: Any):
    instances = {}

    def instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return instance
