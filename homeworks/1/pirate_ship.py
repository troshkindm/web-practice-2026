n, m = map(int, input().split())
items = []

for _ in range(m):
    parts = input().split()
    name = parts[0]
    weight = int(parts[1])
    cost = int(parts[2])
    items.append((name, weight, cost, cost / weight))

items.sort(key=lambda x: -x[3])

result = []
remaining = n

for name, weight, cost, ratio in items:
    if remaining <= 0:
        break
    take = min(weight, remaining)
    fraction = take / weight
    taken_cost = cost * fraction
    result.append((name, take, taken_cost))
    remaining -= take

for name, w, c in result:
    if w == int(w) and c == int(c):
        print(f"{name} {int(w)} {int(c)}")
    else:
        print(f"{name} {w:.2f} {c:.2f}")
