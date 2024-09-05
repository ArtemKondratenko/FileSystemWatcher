import logging
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from filesystemwatcher.polling import watch_directory
from monitoringparser.monitoring_list_parser import load


logging.basicConfig(
    filename='/home/tema/PycharmProjects/FileSystemWatcher/daemon.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def run(MONITORING_LIST: Path) -> None:
    logging.info('Демон запущен')  # Это должно записаться
    logging.info('Вход в основной цикл')  # Это должно записаться

    with ThreadPoolExecutor() as executor:
        while True:
            logging.info('Цикл демона выполняется')  # Это должно записаться
            try:
                with open(MONITORING_LIST, 'r') as file:
                    paths = load(file)
                    logging.info(f'Наблюдение за путями: {paths}')
                    for path in paths:
                        executor.submit(watch_directory, path)
                time.sleep(1)
            except Exception as e:
                logging.error(f'Ошибка в run: {e}')

#
# if __name__ == "__main__":
#     try:
#         with DaemonContext():
#             run()
#     except Exception as e:
#         logging.error(f'Ошибка при запуске демона: {e}')