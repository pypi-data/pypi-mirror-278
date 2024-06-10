from rl_test_common import Common
from rl_test_task_2.client import Client

from .base.task_executor import TaskExecutor


class Task2Executor(TaskExecutor):
    __common: Common = Common()

    def execute(self, request: str) -> None:
        if request == '2':
            self.__common.clear_screen()

            source_file_path: str = input('Source file path: ')
            destination_dir_path: str = input('Destination directory path: ')

            self.__common.clear_screen()

            client: Client = Client()
            client.client_code(source_file_path, destination_dir_path)

        else:
            return super().execute(request)
