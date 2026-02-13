n, m = map(int, input().split())
arr = list(map(int, input().split()))
a = set(map(int, input().split()))
b = set(map(int, input().split()))

mood = 0
for x in arr:
    if x in a:
        mood += 1
    elif x in b:
        mood -= 1

print(mood)
