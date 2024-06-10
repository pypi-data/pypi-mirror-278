from abc import abstractmethod

from .executor import Executor


class TaskExecutor(Executor):
    _next_executor: Executor | None = None

    def set_next(self, executor: Executor) -> Executor:
        self._next_executor = executor
        return executor

    @abstractmethod
    def execute(self, request: str) -> None:
        if self._next_executor:
            return self._next_executor.execute(request)
