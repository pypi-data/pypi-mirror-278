from .base.task_executor import TaskExecutor
from .task_1_executor import Task1Executor
from .task_2_executor import Task2Executor
from .task_3_executor import Task3Executor


class TaskChain:
    @staticmethod
    def get() -> TaskExecutor:
        task_executors: list[TaskExecutor] = [
            Task1Executor(),
            Task2Executor(),
            Task3Executor()
        ]

        task_executors[0].set_next(
            task_executors[1]).set_next(task_executors[2])

        return task_executors[0]
