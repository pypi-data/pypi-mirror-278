#
# Created on Fri May 31 2024
# Copyright (c) 2024 Huy Truong
# ------------------------------
# Purpose: Store problems
# ------------------------------
#
from abc import ABC, abstractmethod
from typing import Literal, Optional, Any

class Experiment(ABC):
    task : Literal['supervised','semi']

    @abstractmethod
    def get_dimensions(self, axis: int = -1) -> tuple[int, Optional[int], int]:
        pass

    @abstractmethod
    def get_data(self, *args,**kwargs)-> tuple[Any, Any, Any]:
        pass

    