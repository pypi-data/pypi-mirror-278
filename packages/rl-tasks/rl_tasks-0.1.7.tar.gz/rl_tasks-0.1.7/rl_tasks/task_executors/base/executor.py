from abc import ABC, abstractmethod
from typing import Any


class Executor(ABC):
    @abstractmethod
    def set_next(self, executor: Any) -> Any:
        pass

    @abstractmethod
    def execute(self, request: Any) -> None:
        pass
