from rl_test_common import Common
from rl_test_task_3.client import Client

from .base.task_executor import TaskExecutor


class Task3Executor(TaskExecutor):
    __common: Common = Common()

    def execute(self, request: str) -> None:
        if request == '3':
            self.__common.clear_screen()

            client: Client = Client()
            client.client_code()

        else:
            return super().execute(request)
