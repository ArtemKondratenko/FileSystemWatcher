from pathlib import Path
from filesystemwatcher.directory import DirectoryState
import logging

def watch_directory(path: Path) -> None:
    logging.info(f'Начато отслеживание директории: {path}')
    try:
        previous_directory_state = DirectoryState(path)
        while True:
            current_directory_state = DirectoryState(path)

            if previous_directory_state != current_directory_state:
                differences = previous_directory_state.differences(current_directory_state)
                for difference in differences:
                    logging.info(f"Изменение: {difference}")
            previous_directory_state = current_directory_state
    except Exception as e:
        logging.error(f'Ошибка в watch_directory для {path}: {e}')


