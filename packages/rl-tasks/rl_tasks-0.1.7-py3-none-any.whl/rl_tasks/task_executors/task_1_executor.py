from rl_test_common import Common
from rl_test_task_1.client import Client

from .base.task_executor import TaskExecutor


class Task1Executor(TaskExecutor):
    __common: Common = Common()

    def execute(self, request: str) -> None:
        if request == '1':
            client: Client = Client()
            client.client_code()

            self.__common.clear_screen()

        else:
            return super().execute(request)
