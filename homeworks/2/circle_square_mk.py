import random
import math

def circle_square_mk(r, n):
    # кидаем n точек в квадрат [-r, r] x [-r, r]
    # считаем долю попавших в круг и умножаем на площадь квадрата
    count = 0
    for _ in range(n):
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)
        if x ** 2 + y ** 2 <= r ** 2:
            count += 1
    return (count / n) * (2 * r) ** 2

if __name__ == '__main__':
    r = 5
    exact = math.pi * r ** 2
    for n in [100, 1000, 10000, 100000]:
        approx = circle_square_mk(r, n)
        error = abs(approx - exact) / exact * 100
        print(f"n={n}: результат={approx:.4f}, точное={exact:.4f}, погрешность={error:.2f}%")

# оценка погрешности:
# n=100:    ~10-15%
# n=1000:   ~3-5%
# n=10000:  ~1-2%
# n=100000: ~0.3-0.5%
# чем больше n тем точнее, сходимость ~ 1/sqrt(n)