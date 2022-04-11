import os
from abc import ABC, abstractmethod
from pathlib import Path


class Base(ABC):
    def __init__(
        self,
        data_dir: Path = "data",
        res_dir: Path = "resources",
        rdf_dir: Path = "rdf",
        is_init: bool = True
    ):
        self.data_dir = Path(data_dir)
        self.res_dir = Path(res_dir)
        self.rdf_dir = Path(rdf_dir)
        if not is_init:
            self._initialize_dirs()

    def _initialize_dirs(self):
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.rdf_dir, exist_ok=True)

    @abstractmethod
    def run(self):
        raise NotImplementedError
