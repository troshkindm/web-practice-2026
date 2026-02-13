s = input()
vowels = 'AEIOU'

kevin = 0
stuart = 0

n = len(s)
for i in range(n):
    if s[i] in vowels:
        kevin += n - i
    else:
        stuart += n - i

if kevin > stuart:
    print("Кевин", kevin)
elif stuart > kevin:
    print("Стюарт", stuart)
else:
    print("Draw")
