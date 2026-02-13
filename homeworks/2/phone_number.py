#  заполняем декоратор wrapper
#  нормализуем номера и форматируем в +7 (xxx) xxx-xx-xx
def wrapper(f):
    def fun(l):
        # нормализуем: убираем всё кроме цифр, отрезаем код страны если 11 цифр
        def normalize(phone):
            digits = ''.join(c for c in phone if c.isdigit())
            if len(digits) == 11:
                digits = digits[1:]
            return digits

        def fmt(phone):
            d = normalize(phone)
            return f"+7 ({d[:3]}) {d[3:6]}-{d[6:8]}-{d[8:10]}"

        # сортируем через оригинальную функцию, потом форматируем
        sorted_phones = f(l)
        return [fmt(p) for p in sorted_phones]
    return fun

@wrapper
def sort_phone(l):
    return sorted(l)

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')