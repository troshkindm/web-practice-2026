import functools
from datetime import datetime

# декоратор, пишущий лог вызова функции в файл
def function_logger(filepath):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = end_time - start_time

            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(f"{func.__name__}\n")
                f.write(f"{start_time}\n")
                # аргументы: позиционные как кортеж, ключевые как словарь
                if args:
                    f.write(f"{args}\n")
                if kwargs:
                    f.write(f"{kwargs}\n")
                # если функция ничего не вернула — пишем '-'
                f.write(f"{result if result is not None else '-'}\n")
                f.write(f"{end_time}\n")
                f.write(f"{duration}\n")

            return result
        return wrapper
    return decorator

if __name__ == '__main__':
    @function_logger('test.log')
    def greeting_format(name):
        return f'Hello, {name}!'

    greeting_format('John')