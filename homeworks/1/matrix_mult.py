n = int(input())

a = []
for _ in range(n):
    row = list(map(int, input().split()))
    a.append(row)

b = []
for _ in range(n):
    row = list(map(int, input().split()))
    b.append(row)

c = [[0] * n for _ in range(n)]

for i in range(n):
    for j in range(n):
        for k in range(n):
            c[i][j] += a[i][k] * b[k][j]

for row in c:
    print(' '.join(map(str, row)))
