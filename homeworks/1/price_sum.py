adult = 0
pensioner = 0
child = 0

with open('products.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f:
        parts = line.strip().split(',')
        if len(parts) >= 4:
            adult += float(parts[1])
            pensioner += float(parts[2])
            child += float(parts[3])

print(f"{adult:.2f} {pensioner:.2f} {child:.2f}")
