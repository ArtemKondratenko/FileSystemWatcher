import logging
import signal
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from filesystemwatcher.daemon_control import is_running
from filesystemwatcher.polling import watch_directory
from monitoringparser.monitoring_list_parser import load


logging.basicConfig(
    filename='/home/tema/PycharmProjects/FileSystemWatcher/daemon.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def run(MONITORING_LIST: Path) -> None:
    logging.info('Демон запущен')
    logging.info('Вход в основной цикл')

    monitored_paths = set()  # Для хранения отслеживаемых путей
    with ThreadPoolExecutor() as executor:
        while is_running():  # Проверяем флаг
            logging.info('Цикл демона выполняется')
            try:
                with open(MONITORING_LIST, 'r') as file:
                    paths = load(file)
                    logging.info(f'Наблюдение за путями: {paths}')
                    new_paths = set(paths)

                    # Проверяем новые и старые пути
                    added_paths = new_paths - monitored_paths
                    removed_paths = monitored_paths - new_paths

                    # Добавляем новые пути
                    for path in added_paths:
                        logging.info(f'Добавлен путь: {path}')
                        executor.submit(watch_directory, path)

                    # Удаляем старые пути
                    for path in removed_paths:
                        logging.info(f'Удален путь: {path}')

                    # Обновляем отслеживаемые пути
                    monitored_paths = new_paths

                time.sleep(5)
            except Exception as e:
                logging.error(f'Ошибка в run: {e}')
                time.sleep(5)

#
# if __name__ == "__main__":
#     try:
#         with DaemonContext():
#             run()
#     except Exception as e:
#         logging.error(f'Ошибка при запуске демона: {e}')