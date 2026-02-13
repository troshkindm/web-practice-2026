import sys

# рекурсивный факториал — вызывает сам себя, пока не дойдёт до базового случая
def fact_rec(n):
    if n <= 1:
        return 1
    return n * fact_rec(n - 1)

# итеративный — просто цикл, без накладных расходов на стек вызовов
def fact_it(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

if __name__ == '__main__':
    import time

    # без этого рекурсивный вариант упадёт на больших n
    sys.setrecursionlimit(10**5 + 100)
    n = 950

    start = time.time()
    fact_rec(n)
    rec_time = time.time() - start
    print(f"рекурсивный: {rec_time:.6f}с")

    start = time.time()
    fact_it(n)
    it_time = time.time() - start
    print(f"итеративный: {it_time:.6f}с")

# итеративный быстрее за счёт отсутствия оверхеда на вызовы функций
# рекурсивный упирается в лимит стека (~1000 по умолчанию)
# для n=950: рекурсивный ~0.002с, итеративный ~0.001с