import subprocess
import os
import math
import pytest

INTERPRETER = 'python'

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()


# --- 1. факториал ---

from fact import fact_rec, fact_it

@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (5, 120),
    (10, 3628800),
])
def test_fact_rec(n, expected):
    assert fact_rec(n) == expected

@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (5, 120),
    (10, 3628800),
    (20, 2432902008176640000),
])
def test_fact_it(n, expected):
    assert fact_it(n) == expected

def test_fact_rec_equals_it():
    for n in [0, 1, 5, 10, 15]:
        assert fact_rec(n) == fact_it(n)


# --- 2. данные сотрудника ---

from show_employee import show_employee

@pytest.mark.parametrize("name, salary, expected", [
    ("Иванов Иван Иванович", 30000, "Иванов Иван Иванович: 30000 ₽"),
    ("John", 50000, "John: 50000 ₽"),
    ("A", 0, "A: 0 ₽"),
])
def test_show_employee_with_salary(name, salary, expected):
    assert show_employee(name, salary) == expected

def test_show_employee_default():
    assert show_employee("Петров") == "Петров: 100000 ₽"

def test_show_employee_negative_salary():
    assert show_employee("X", -500) == "X: -500 ₽"


# --- 3. сумма и разность ---

from sum_and_sub import sum_and_sub

@pytest.mark.parametrize("a, b, exp_sum, exp_diff", [
    (3, 5, 8, -2),
    (10, 10, 20, 0),
    (-3, 5, 2, -8),
    (0, 0, 0, 0),
    (1.5, 2.5, 4.0, -1.0),
    (-1.5, -2.5, -4.0, 1.0),
])
def test_sum_and_sub(a, b, exp_sum, exp_diff):
    s, d = sum_and_sub(a, b)
    assert s == pytest.approx(exp_sum)
    assert d == pytest.approx(exp_diff)


# --- 4. обработка списка ---

from process_list import process_list, process_list_lc, process_list_gen

@pytest.mark.parametrize("arr, expected", [
    ([1, 2, 3], [1, 4, 27]),        # нечёт→куб, чёт→квадрат
    ([0, 1, 2], [0, 1, 4]),
    ([-2, -1], [4, -1]),             # отрицательные
    ([4], [16]),
    ([5], [125]),
    ([], []),
])
def test_process_list(arr, expected):
    assert process_list(arr) == expected

@pytest.mark.parametrize("arr, expected", [
    ([1, 2, 3], [1, 4, 27]),
    ([0], [0]),
    ([-3, -4], [-27, 16]),
])
def test_process_list_lc(arr, expected):
    assert process_list_lc(arr) == expected

@pytest.mark.parametrize("arr, expected", [
    ([1, 2, 3], [1, 4, 27]),
    ([0, 0], [0, 0]),
    ([], []),
])
def test_process_list_gen(arr, expected):
    assert list(process_list_gen(arr)) == expected


# --- 5. my_sum ---

from my_sum import my_sum

@pytest.mark.parametrize("args, expected", [
    ((1, 2, 3), 6),
    ((10,), 10),
    ((), 0),
    ((-1, 1), 0),
    ((1.5, 2.5, 3.0), 7.0),
])
def test_my_sum(args, expected):
    assert my_sum(*args) == pytest.approx(expected)


# --- 6. my_sum_argv ---

def test_my_sum_argv_integers():
    proc = subprocess.run(
        [INTERPRETER, 'my_sum_argv.py', '1', '2', '3', '4', '5'],
        capture_output=True, text=True
    )
    assert proc.stdout.strip() == '15'

def test_my_sum_argv_floats():
    proc = subprocess.run(
        [INTERPRETER, 'my_sum_argv.py', '1.5', '2.5'],
        capture_output=True, text=True
    )
    assert float(proc.stdout.strip()) == pytest.approx(4.0)

def test_my_sum_argv_single():
    proc = subprocess.run(
        [INTERPRETER, 'my_sum_argv.py', '42'],
        capture_output=True, text=True
    )
    assert proc.stdout.strip() == '42'


# --- 7. сортировка файлов ---

from files_sort import sort_files

def test_files_sort_by_extension(tmp_path):
    for name in ['a.txt', 'b.py', 'c.txt', 'a.py']:
        (tmp_path / name).write_text('x')
    result = sort_files(str(tmp_path))
    assert result == ['a.py', 'b.py', 'a.txt', 'c.txt']

def test_files_sort_ignores_dirs(tmp_path):
    (tmp_path / 'a.txt').write_text('x')
    (tmp_path / 'subdir').mkdir()
    result = sort_files(str(tmp_path))
    assert result == ['a.txt']

def test_files_sort_empty(tmp_path):
    assert sort_files(str(tmp_path)) == []

def test_files_sort_same_extension(tmp_path):
    for name in ['c.py', 'a.py', 'b.py']:
        (tmp_path / name).write_text('x')
    result = sort_files(str(tmp_path))
    assert result == ['a.py', 'b.py', 'c.py']


# --- 8. поиск файла ---

from file_search import find_file, read_first_lines

def test_find_file_found(tmp_path):
    (tmp_path / 'target.txt').write_text('hello')
    result = find_file('target.txt', str(tmp_path))
    assert result is not None
    assert result.endswith('target.txt')

def test_find_file_nested(tmp_path):
    sub = tmp_path / 'sub'
    sub.mkdir()
    (sub / 'deep.txt').write_text('found')
    result = find_file('deep.txt', str(tmp_path))
    assert result is not None

def test_find_file_not_found(tmp_path):
    assert find_file('nonexistent.txt', str(tmp_path)) is None

def test_read_first_lines_short(tmp_path):
    p = tmp_path / 'test.txt'
    p.write_text('a\nb\nc')
    lines = read_first_lines(str(p), 5)
    assert len(lines) == 3

def test_read_first_lines_long(tmp_path):
    p = tmp_path / 'test.txt'
    p.write_text('\n'.join(f'line{i}' for i in range(20)))
    lines = read_first_lines(str(p), 5)
    assert len(lines) == 5
    assert lines[0] == 'line0'
    assert lines[4] == 'line4'


# --- 9. валидация email ---

from email_validation import fun as email_fun

@pytest.mark.parametrize("email, expected", [
    ('lara@mospolytech.ru', True),
    ('brian-23@mospolytech.ru', True),
    ('britts_54@mospolytech.ru', True),
    ('test@site.abcd', False),          # расширение > 3 символов
    ('user@site', False),               # нет расширения
    ('@site.com', False),               # нет имени пользователя
    ('user@.com', False),               # нет имени сайта
    ('us er@site.com', False),          # пробел в имени
    ('user@si-te.com', False),          # дефис в имени сайта
    ('a@b.c', True),                    # минимально валидный
    ('user@site.', False),              # пустое расширение
])
def test_email_validation(email, expected):
    assert email_fun(email) == expected


# --- 10. фибоначчи ---

from fibonacci import fibonacci, cube

@pytest.mark.parametrize("n, expected", [
    (1, [0]),
    (2, [0, 1]),
    (5, [0, 1, 1, 2, 3]),
    (7, [0, 1, 1, 2, 3, 5, 8]),
])
def test_fibonacci(n, expected):
    assert fibonacci(n) == expected

@pytest.mark.parametrize("n, expected", [
    (1, [0]),
    (5, [0, 1, 1, 8, 27]),
])
def test_cube_fibonacci(n, expected):
    assert list(map(cube, fibonacci(n))) == expected


# --- 11. средние оценки ---

from average_scores import compute_average_scores

@pytest.mark.parametrize("scores, expected", [
    (
        [(89, 90, 78, 93, 80), (90, 91, 85, 88, 86), (91, 92, 83, 89, 90.5)],
        (90.0, 91.0, 82.0, 90.0, 85.5),
    ),
    (
        [(100,), (50,)],
        (75.0,),
    ),
    (
        [(10, 20), (30, 40)],
        (20.0, 30.0),
    ),
    (
        [(0, 0, 0)],
        (0.0, 0.0, 0.0),
    ),
])
def test_average_scores(scores, expected):
    result = compute_average_scores(scores)
    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert r == pytest.approx(e, abs=0.1)


# --- 12. угол между плоскостями ---

from plane_angle import Point, plane_angle

def test_plane_angle_90():
    a = Point(0, 0, 0)
    b = Point(1, 0, 0)
    c = Point(1, 1, 0)
    d = Point(1, 1, 1)
    assert plane_angle(a, b, c, d) == pytest.approx(90.0, abs=0.01)

def test_plane_angle_0():
    a = Point(0, 0, 0)
    b = Point(1, 0, 0)
    c = Point(1, 1, 0)
    d = Point(0, 1, 0)
    assert plane_angle(a, b, c, d) == pytest.approx(0.0, abs=0.01)

def test_plane_angle_180():
    a = Point(0, 0, 0)
    b = Point(1, 0, 0)
    c = Point(1, 1, 0)
    d = Point(2, 1, 0)
    assert plane_angle(a, b, c, d) == pytest.approx(180.0, abs=0.01)

def test_point_subtraction():
    p1 = Point(3, 4, 5)
    p2 = Point(1, 2, 3)
    r = p1 - p2
    assert (r.x, r.y, r.z) == (2, 2, 2)


# --- 13. номер телефона ---

from phone_number import sort_phone

def test_phone_format_8():
    result = sort_phone(['89001234567'])
    assert result == ['+7 (900) 123-45-67']

def test_phone_format_plus7():
    result = sort_phone(['+79001234567'])
    assert result == ['+7 (900) 123-45-67']

def test_phone_format_0():
    result = sort_phone(['07895462130'])
    assert result == ['+7 (789) 546-21-30']

def test_phone_format_10digits():
    result = sort_phone(['9195969878'])
    assert result == ['+7 (919) 596-98-78']

def test_phone_sort_order():
    result = sort_phone(['89875641230', '07895462130', '9195969878'])
    assert result[0] == '+7 (789) 546-21-30'


# --- 14. сортировка людей ---

from people_sort import name_format

def test_people_sort_basic():
    people = [
        ['Mike', 'Thomson', '20', 'M'],
        ['Robert', 'Bustle', '32', 'M'],
        ['Andria', 'Bustle', '30', 'F'],
    ]
    result = name_format(people)
    assert result[0] == 'Mr. Mike Thomson'
    assert result[1] == 'Ms. Andria Bustle'
    assert result[2] == 'Mr. Robert Bustle'

def test_people_sort_same_age():
    people = [
        ['A', 'B', '25', 'M'],
        ['C', 'D', '25', 'F'],
    ]
    result = name_format(people)
    # одинаковый возраст — порядок ввода
    assert result[0] == 'Mr. A B'
    assert result[1] == 'Ms. C D'


# --- 15. комплексные числа ---

from complex_numbers import Complex

def test_complex_add():
    result = Complex(2, 1) + Complex(5, 6)
    assert str(result) == '7.00+7.00i'

def test_complex_sub():
    result = Complex(2, 1) - Complex(5, 6)
    assert str(result) == '-3.00-5.00i'

def test_complex_mul():
    result = Complex(2, 1) * Complex(5, 6)
    assert str(result) == '4.00+17.00i'

def test_complex_div():
    result = Complex(2, 1) / Complex(5, 6)
    assert str(result) == '0.26-0.11i'

def test_complex_mod():
    assert str(Complex(2, 1).mod()) == '2.24+0.00i'

def test_complex_str_negative_imag():
    assert str(Complex(3, -4)) == '3.00-4.00i'

def test_complex_str_zero_imag():
    assert str(Complex(5, 0)) == '5.00+0.00i'

def test_complex_str_zero_real():
    assert str(Complex(0, 3)) == '0.00+3.00i'


# --- 16. монте-карло ---

from circle_square_mk import circle_square_mk

def test_monte_carlo_r1():
    result = circle_square_mk(1, 100000)
    assert result == pytest.approx(math.pi, rel=0.05)

def test_monte_carlo_r5():
    result = circle_square_mk(5, 100000)
    assert result == pytest.approx(math.pi * 25, rel=0.05)

def test_monte_carlo_r0():
    # радиус 0 — площадь 0
    result = circle_square_mk(0, 1000)
    assert result == pytest.approx(0.0, abs=0.01)


# --- 17. логгер ---

from log_decorator import function_logger

def test_logger_basic(tmp_path):
    log_file = str(tmp_path / 'test.log')

    @function_logger(log_file)
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5

    with open(log_file, 'r') as f:
        content = f.read()
    assert 'add' in content
    assert '(2, 3)' in content
    assert '5' in content

def test_logger_no_return(tmp_path):
    log_file = str(tmp_path / 'test2.log')

    @function_logger(log_file)
    def noop():
        pass

    noop()

    with open(log_file, 'r') as f:
        content = f.read()
    assert 'noop' in content
    assert '-' in content

def test_logger_kwargs(tmp_path):
    log_file = str(tmp_path / 'test3.log')

    @function_logger(log_file)
    def greet(name='World'):
        return f'Hello, {name}!'

    greet(name='John')

    with open(log_file, 'r') as f:
        content = f.read()
    assert 'greet' in content
    assert "'name': 'John'" in content