import time
from pathlib import Path
from filesystemwatcher.directory import DirectoryState
import logging
from filesystemwatcher.daemon_control import is_running

def watch_directory(path: Path) -> None:
    logging.info(f'Начато отслеживание директории: {path}')
    try:
        previous_directory_state = DirectoryState(path)
        while is_running():  # Проверяем флаг
            current_directory_state = DirectoryState(path)

            if previous_directory_state != current_directory_state:
                differences = previous_directory_state.differences(current_directory_state)
                for difference in differences:
                    logging.info(f"Изменение: {difference}")
            previous_directory_state = current_directory_state
            time.sleep(1)  # Ожидание перед следующим сравнением
    except Exception as e:
        logging.error(f'Ошибка в watch_directory для {path}: {e}')


