#  то же самое, но числа берутся из аргументов командной строки
import sys

def my_sum(*args):
    return sum(args)

if __name__ == '__main__':
    numbers = [float(x) for x in sys.argv[1:]]
    result = my_sum(*numbers)
    # если результат целый — выводим без .0
    print(int(result) if result == int(result) else result)