#  заполняем декоратор person_lister. сортировка по возрасту, форматирование Mr./Ms.
def person_lister(f):
    def inner(people):
        # сортируем по возрасту (индекс 2), для одинаковых — порядок ввода (stable sort)
        sorted_people = sorted(people, key=lambda p: int(p[2]))
        return [f(person) for person in sorted_people]
    return inner

@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    people = [input().split() for i in range(int(input()))]
    print(*name_format(people), sep='\n')