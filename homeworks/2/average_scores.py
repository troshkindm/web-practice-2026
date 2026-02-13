# средние баллы студентов
# scores — список кортежей по предметам,
# надо посчитать среднее для каждого студента (по столбцам)
def compute_average_scores(scores):
    if not scores:
        return ()
    n_students = len(scores[0])
    n_subjects = len(scores)
    averages = []
    for i in range(n_students):
        total = sum(s[i] for s in scores)
        averages.append(total / n_subjects)
    return tuple(averages)

if __name__ == '__main__':
    n, x = map(int, input().split())
    scores = []
    for _ in range(x):
        row = tuple(map(float, input().split()))
        scores.append(row)
    result = compute_average_scores(scores)
    for avg in result:
        print(f"{avg:.1f}")
        