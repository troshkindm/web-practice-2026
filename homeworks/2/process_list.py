# оригинальная функция: чётные → квадрат, нечётные → куб.
def process_list(arr):
    result = []
    for i in arr:
        if i % 2 == 0:
            result.append(i**2)
        else:
            result.append(i**3)
    return result

# то же самое через list comprehension — короче и чуть быстрее
def process_list_lc(arr):
    return [i**2 if i % 2 == 0 else i**3 for i in arr]

# генератор — не создаёт список в памяти целиком, отдаёт по одному
def process_list_gen(arr):
    for i in arr:
        if i % 2 == 0:
            yield i**2
        else:
            yield i**3

if __name__ == '__main__':
    import time

    arr = list(range(-500, 501))

    start = time.time()
    for _ in range(10000):
        process_list_lc(arr)
    lc_time = time.time() - start

    start = time.time()
    for _ in range(10000):
        list(process_list_gen(arr))
    gen_time = time.time() - start

    print(f"list comprehension: {lc_time:.4f}с")
    print(f"генератор: {gen_time:.4f}с")

# lc и генератор работают примерно одинаково по скорости
# генератор выигрывает по памяти на больших данных если не нужен весь список сразу
# lc чуть быстрее если результат всё равно нужен целиком