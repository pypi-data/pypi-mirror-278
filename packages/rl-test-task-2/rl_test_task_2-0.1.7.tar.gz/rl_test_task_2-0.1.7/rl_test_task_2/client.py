import logging
import os
import shutil
from pathlib import Path


class Client:
    __logger: logging.Logger = logging.getLogger(__name__)

    def client_code(self, source_file_path_as_str: str, destination_path_as_str: str) -> None:
        source_file_path: Path = Path(source_file_path_as_str)
        destination_path: Path = Path(destination_path_as_str)

        self.__try_move(source_file_path, destination_path)
        self.__print_destination_file_path(source_file_path, destination_path)

    def __try_move(self, source_file_path: Path, destination_path: Path) -> None:
        try:
            shutil.move(source_file_path, destination_path)

        except FileNotFoundError:
            self.__logger.error(f'Source file not found: {source_file_path}.')

        except PermissionError as e:
            self.__logger.error(e)

    def __print_destination_file_path(self, source_file_path: Path, destination_path: Path) -> None:
        if destination_path.is_file:
            print(destination_path)

        elif destination_path.is_dir:
            destination_file_path: str = os.path.join(
                destination_path,
                os.path.basename(source_file_path))

            print(destination_file_path)
