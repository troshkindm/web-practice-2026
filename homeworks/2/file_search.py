#  рекурсивный поиск файла через os.walk, вывод первых 5 строк
import os
import sys

def find_file(filename, start_dir=None):
    if start_dir is None:
        start_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None

def read_first_lines(filepath, n=5):
    lines = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            lines.append(line.rstrip('\n'))
    return lines

if __name__ == '__main__':
    filename = sys.argv[1]
    result = find_file(filename)
    if result:
        for line in read_first_lines(result):
            print(line)
    else:
        print(f"Файл {filename} не найден")