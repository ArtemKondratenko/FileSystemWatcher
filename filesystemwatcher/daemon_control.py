running = True

def stop():
    global running
    running = False  # Устанавливаем флаг в False для завершения работы

def is_running():
    return running  # Возвращаем текущее состояние