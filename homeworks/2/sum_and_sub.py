# возвращает кортеж (сумма, разность)
def sum_and_sub(a, b):
    return a + b, a - b

if __name__ == '__main__':
    a, b = map(float, input().split())
    s, d = sum_and_sub(a, b)
    print(s, d)