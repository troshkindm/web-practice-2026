n = int(input())
scores = list(map(int, input().split()))

unique = sorted(set(scores), reverse=True)
print(unique[1])
