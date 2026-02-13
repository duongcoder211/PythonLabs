import sys
import logging
import io
from functools import wraps

def logger(func=None, *, handle=sys.stdout):
    """
    Декоратор для логирования вызовов функций.

    Параметры:
        func (callable, optional): Декорируемая функция (используется при вызове без параметров).
        handle (object, optional): Обработчик логов (sys.stdout, объект файла с .write(),
                                  или объект logging.Logger). По умолчанию sys.stdout.
    """

    # Определяем, используем ли мы модуль logging или метод .write()
    is_logging_logger = isinstance(handle, logging.Logger)
    is_logging_stream = isinstance(handle, io.StringIO)

    def decorator(fn):
        @wraps(fn) #Сохраяем сигнатуру исходной функции (__name__, docstring)
        def wrapper(*args, **kwargs):
            # Форматируем аргументы для лога
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            
            start_message = f"Function {fn.__name__} starting with args ({signature})\n"

            try:
                # Логируем старт вызова
                if is_logging_logger:
                    handle.info(start_message.strip())
                elif is_logging_stream:
                    handle.write("INFO: " + start_message)
                else:
                    handle.write("INFO: " + start_message)
                    if handle is sys.stdout:
                        handle.flush() # Обеспечивает немедленный вывод в stdout

                # Вызываем оригинальную функцию
                result = fn(*args, **kwargs)
                
                # Логируем успешное завершение
                end_message = f"Function {fn.__name__} finished successfully with result {result!r}\n"
                if is_logging_logger:
                    handle.info(end_message.strip())
                elif is_logging_stream:
                    handle.write("INFO: " + end_message)
                else:
                    handle.write("INFO: " + end_message)
                    if handle is sys.stdout:
                        handle.flush()

                return result

            except Exception as e:
                # Логируем исключение и повторно его выбрасываем
                error_message = f"Exception {type(e).__name__}: {e} occurred in function {fn.__name__}\n"
                if is_logging_logger:
                    handle.error(error_message.strip() + "\n")
                elif is_logging_stream:
                    handle.write("ERROR: " + error_message)
                else:
                    handle.write("ERROR: " + error_message)
                    if handle is sys.stdout:
                        handle.flush()
                raise e

        return wrapper

    # Если декоратор вызван без параметров (@logger), func будет самой функцией.
    # Если с параметрами (@logger(handle=...)), func будет None, и мы возвращаем decorator.
    if func is not None:
        return decorator(func)
    else:
        return decorator
