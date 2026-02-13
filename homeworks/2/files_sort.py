# сортировка файлов в директории по расширению, потом по имени
import os
import sys

def sort_files(directory):
    # берём только файлы, каталоги пропускаем
    files = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]
    # ключ сортировки: сначала расширение, потом имя
    files.sort(key=lambda f: (os.path.splitext(f)[1], os.path.splitext(f)[0]))
    return files

if __name__ == '__main__':
    directory = sys.argv[1]
    for f in sort_files(directory):
        print(f)