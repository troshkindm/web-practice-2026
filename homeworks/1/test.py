import subprocess
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

# 1. hello.py
def test_hello():
    assert run_script('hello.py') == 'Hello, World!'

def test_hello_no_extra_output():
    result = run_script('hello.py')
    assert result.count('\n') == 0

# 2. python_if_else.py
@pytest.mark.parametrize("input_data, expected", [
    ('1', 'Weird'),       # odd, min boundary
    ('3', 'Weird'),       # odd
    ('5', 'Weird'),       # odd
    ('7', 'Weird'),       # odd
    ('99', 'Weird'),      # odd, near max
    ('2', 'Not Weird'),   # even, range 2-5
    ('4', 'Not Weird'),   # even, range 2-5
    ('6', 'Weird'),       # even, range 6-20, boundary
    ('8', 'Weird'),       # even, range 6-20
    ('20', 'Weird'),      # even, range 6-20, boundary
    ('22', 'Not Weird'),  # even, >20, boundary
    ('100', 'Not Weird'), # even, >20, max boundary
])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

# 3. arithmetic_operators.py
@pytest.mark.parametrize("input_data, expected", [
    (['1', '1'], ['2', '0', '1']),
    (['1', '2'], ['3', '-1', '2']),
    (['10', '5'], ['15', '5', '50']),
    (['0', '5'], ['5', '-5', '0']),
    (['7', '3'], ['10', '4', '21']),
    (['100', '100'], ['200', '0', '10000']),
    (['10000000000', '10000000000'], ['20000000000', '0', '100000000000000000000']),  # 10^10 boundary
    (['1', '10000000000'], ['10000000001', '-9999999999', '10000000000']),
])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

# 4. division.py
@pytest.mark.parametrize("input_data, expected", [
    (['10', '3'], ['3', '3.3333333333333335']),
    (['10', '2'], ['5', '5.0']),
    (['7', '2'], ['3', '3.5']),
    (['0', '5'], ['0', '0.0']),
    (['15', '4'], ['3', '3.75']),
    (['1', '1'], ['1', '1.0']),
    (['-10', '3'], ['-4', '-3.3333333333333335']),   # negative numerator
    (['10', '-3'], ['-4', '-3.3333333333333335']),    # negative denominator
    (['-10', '-3'], ['3', '3.3333333333333335']),     # both negative
    (['-7', '2'], ['-4', '-3.5']),                    # negative floor division
    (['0', '1'], ['0', '0.0']),                       # zero numerator
])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected

def test_division_by_zero():
    result = run_script('division.py', ['5', '0'])
    assert 'Error' in result or 'error' in result.lower()

def test_division_by_zero_negative():
    result = run_script('division.py', ['-5', '0'])
    assert 'Error' in result or 'error' in result.lower()

def test_division_zero_by_zero():
    result = run_script('division.py', ['0', '0'])
    assert 'Error' in result or 'error' in result.lower()

# 5. loops.py
@pytest.mark.parametrize("input_data, expected", [
    ('1', ['0']),
    ('2', ['0', '1']),
    ('3', ['0', '1', '4']),
    ('5', ['0', '1', '4', '9', '16']),
    ('10', ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81']),
    ('20', ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81',
            '100', '121', '144', '169', '196', '225', '256', '289', '324', '361']),  # max boundary
])
def test_loops(input_data, expected):
    assert run_script('loops.py', [input_data]).split('\n') == expected

# 6. print_function.py
@pytest.mark.parametrize("input_data, expected", [
    ('1', '1'),
    ('2', '12'),
    ('3', '123'),
    ('5', '12345'),
    ('10', '12345678910'),
    ('20', '1234567891011121314151617181920'),  # max boundary
])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', [input_data]) == expected

# 7. second_score.py
@pytest.mark.parametrize("input_data, expected", [
    (['5', '2 3 6 6 5'], '5'),
    (['3', '1 2 3'], '2'),
    (['4', '5 5 5 4'], '4'),
    (['2', '1 2'], '1'),
    (['5', '10 10 9 8 7'], '9'),
    (['3', '1 1 2'], '1'),           # second is the minimum
    (['4', '100 90 90 80'], '90'),   # duplicates in second place
])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data) == expected

# 8. nested_list.py
@pytest.mark.parametrize("input_data, expected", [
    (['3', 'chi', '20.0', 'beta', '50.0', 'alpha', '50.0'], 'alpha\nbeta'),
    (['5', 'Harry', '37.21', 'Berry', '37.21', 'Tina', '37.2', 'Akriti', '41', 'Harsh', '39'],
     'Berry\nHarry'),
    (['2', 'A', '10', 'B', '20'], 'B'),
    (['3', 'C', '30', 'A', '20', 'B', '10'], 'A'),           # single second lowest
    (['4', 'D', '5', 'C', '5', 'B', '3', 'A', '3'], 'C\nD'), # alphabetical order for second
    (['2', 'Z', '1', 'A', '2'], 'A'),
])
def test_nested_list(input_data, expected):
    assert run_script('nested_list.py', input_data) == expected

# 9. lists.py
def test_lists_basic():
    input_data = ['4', 'append 1', 'append 2', 'insert 1 3', 'print']
    assert run_script('lists.py', input_data) == '[1, 3, 2]'

def test_lists_complex():
    input_data = ['12', 'insert 0 5', 'insert 1 10', 'insert 0 6', 'print',
                  'remove 6', 'append 9', 'append 1', 'sort', 'print',
                  'pop', 'reverse', 'print']
    result = run_script('lists.py', input_data).split('\n')
    assert result == ['[6, 5, 10]', '[1, 5, 9, 10]', '[9, 5, 1]']

def test_lists_sort_reverse():
    input_data = ['5', 'append 3', 'append 1', 'append 2', 'sort', 'print']
    assert run_script('lists.py', input_data) == '[1, 2, 3]'

def test_lists_pop():
    input_data = ['4', 'append 10', 'append 20', 'pop', 'print']
    assert run_script('lists.py', input_data) == '[10]'

def test_lists_reverse():
    input_data = ['5', 'append 1', 'append 2', 'append 3', 'reverse', 'print']
    assert run_script('lists.py', input_data) == '[3, 2, 1]'

def test_lists_remove():
    input_data = ['4', 'append 5', 'append 5', 'remove 5', 'print']
    assert run_script('lists.py', input_data) == '[5]'

def test_lists_multiple_prints():
    input_data = ['6', 'append 1', 'print', 'append 2', 'print', 'append 3', 'print']
    result = run_script('lists.py', input_data).split('\n')
    assert result == ['[1]', '[1, 2]', '[1, 2, 3]']

# 10. swap_case.py
@pytest.mark.parametrize("input_data, expected", [
    ('Www.MosPolytech.ru', 'wWW.mOSpOLYTECH.RU'),
    ('Pythonist 2', 'pYTHONIST 2'),
    ('HeLLo', 'hEllO'),
    ('ABC', 'abc'),
    ('abc', 'ABC'),
    ('123', '123'),
    ('a', 'A'),
    ('Z', 'z'),
    ('Hello World 123!', 'hELLO wORLD 123!'),
])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', [input_data]) == expected

# 11. split_and_join.py
@pytest.mark.parametrize("input_data, expected", [
    ('this is a string', 'this-is-a-string'),
    ('hello world', 'hello-world'),
    ('one', 'one'),
    ('a b c d', 'a-b-c-d'),
    ('hello   world', 'hello-world'),       # multiple spaces
    ('a b', 'a-b'),                          # single chars
])
def test_split_and_join(input_data, expected):
    assert run_script('split_and_join.py', [input_data]) == expected

# 12. max_word.py
def test_max_word_contains_longest():
    result = run_script('max_word.py')
    assert 'сосредоточенности' in result

def test_max_word_no_punctuation_in_result():
    result = run_script('max_word.py')
    for line in result.split('\n'):
        assert line.isalpha()

def test_max_word_not_empty():
    result = run_script('max_word.py')
    assert len(result) > 0

# 13. price_sum.py
def test_price_sum():
    result = run_script('price_sum.py')
    parts = result.split()
    assert len(parts) == 3
    assert float(parts[0]) == pytest.approx(6842.84, rel=0.01)
    assert float(parts[1]) == pytest.approx(5891.06, rel=0.01)
    assert float(parts[2]) == pytest.approx(6810.90, rel=0.01)

def test_price_sum_format():
    result = run_script('price_sum.py')
    parts = result.split()
    for p in parts:
        assert '.' in p
        assert len(p.split('.')[1]) == 2  # exactly 2 decimal places

# 14. anagram.py
@pytest.mark.parametrize("input_data, expected", [
    (['listen', 'silent'], 'YES'),
    (['hello', 'world'], 'NO'),
    (['abc', 'cba'], 'YES'),
    (['abc', 'abcd'], 'NO'),
    (['a', 'a'], 'YES'),
    (['ab', 'ba'], 'YES'),
    (['aab', 'aba'], 'YES'),
    (['abc', 'ABC'], 'NO'),          # case sensitive
    (['aa', 'a'], 'NO'),             # different lengths
    (['abcdef', 'fedcba'], 'YES'),
])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data) == expected

# 15. metro.py
@pytest.mark.parametrize("input_data, expected", [
    (['3', '1 5', '2 8', '6 10', '5'], '2'),
    (['2', '0 10', '5 15', '10'], '2'),         # T at exit time
    (['1', '5 10', '7'], '1'),
    (['2', '1 3', '5 7', '4'], '0'),             # T in gap
    (['3', '0 5', '0 5', '0 5', '3'], '3'),      # all same interval
    (['1', '5 10', '5'], '1'),                    # T at entry time
    (['1', '5 10', '10'], '1'),                   # T at exit time
    (['3', '1 10', '5 15', '10 20', '10'], '3'),  # all present at T=10
    (['1', '0 0', '0'], '1'),                     # entry == exit == T
])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data) == expected

# 16. minion_game.py
@pytest.mark.parametrize("input_data, expected_winner", [
    ('BANANA', 'Стюарт'),
    ('AAAA', 'Кевин'),
    ('BBBB', 'Стюарт'),
])
def test_minion_game(input_data, expected_winner):
    result = run_script('minion_game.py', [input_data])
    assert expected_winner in result

def test_minion_game_banana_score():
    result = run_script('minion_game.py', ['BANANA'])
    assert '12' in result

def test_minion_game_single_vowel():
    result = run_script('minion_game.py', ['A'])
    assert 'Кевин' in result

def test_minion_game_single_consonant():
    result = run_script('minion_game.py', ['B'])
    assert 'Стюарт' in result

# 17. is_leap.py
@pytest.mark.parametrize("input_data, expected", [
    ('2000', 'True'),    # divisible by 400
    ('1900', 'False'),   # divisible by 100 but not 400
    ('2004', 'True'),    # divisible by 4
    ('2100', 'False'),   # divisible by 100
    ('2400', 'True'),    # divisible by 400
    ('2001', 'False'),   # not divisible by 4
    ('2020', 'True'),    # divisible by 4
    ('1904', 'True'),    # boundary + leap
    ('2200', 'False'),   # divisible by 100
    ('100000', 'True'),  # max boundary, 100000 % 400 == 0
    ('1999', 'False'),   # odd year
])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', [input_data]) == expected

# 18. happiness.py
@pytest.mark.parametrize("input_data, expected", [
    (['3 2', '1 5 3', '3 1', '5 7'], '1'),
    (['5 2', '1 2 3 1 2', '1 2', '3 4'], '3'),
    (['3 1', '1 1 1', '1', '2'], '3'),
    (['3 1', '2 2 2', '1', '2'], '-3'),
    (['1 1', '5', '5', '1'], '1'),                   # single element in A
    (['1 1', '5', '1', '5'], '-1'),                   # single element in B
    (['4 2', '1 2 3 4', '1 2', '3 4'], '0'),          # balanced
    (['3 1', '7 7 7', '8', '9'], '0'),                # no matches
])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data) == expected

# 19. pirate_ship.py
def test_pirate_ship_basic():
    input_data = ['10 3', 'gold 5 100', 'silver 3 30', 'bronze 8 40']
    result = run_script('pirate_ship.py', input_data)
    lines = result.strip().split('\n')
    assert lines[0].startswith('gold')

def test_pirate_ship_partial():
    input_data = ['5 2', 'gold 10 100', 'silver 5 25']
    result = run_script('pirate_ship.py', input_data)
    assert 'gold' in result

def test_pirate_ship_all_fit():
    input_data = ['100 2', 'gold 5 100', 'silver 3 30']
    result = run_script('pirate_ship.py', input_data)
    assert 'gold' in result and 'silver' in result

def test_pirate_ship_single_item():
    input_data = ['10 1', 'gold 5 100']
    result = run_script('pirate_ship.py', input_data)
    assert 'gold' in result

def test_pirate_ship_zero_capacity():
    input_data = ['0 2', 'gold 5 100', 'silver 3 30']
    result = run_script('pirate_ship.py', input_data)
    assert result == ''

def test_pirate_ship_exact_output():
    input_data = ['10 3', 'gold 5 100', 'silver 3 30', 'bronze 8 40']
    result = run_script('pirate_ship.py', input_data)
    lines = result.strip().split('\n')
    assert lines[0] == 'gold 5 100'
    assert lines[1] == 'silver 3 30'
    assert lines[2] == 'bronze 2 10'

def test_pirate_ship_partial_float():
    input_data = ['5 2', 'gold 10 100', 'silver 5 25']
    result = run_script('pirate_ship.py', input_data)
    lines = result.strip().split('\n')
    # gold ratio=10, silver ratio=5, берём 5кг gold из 10
    assert lines[0] == 'gold 5 50'

# 20. matrix_mult.py
def test_matrix_mult_2x2():
    input_data = ['2', '1 2', '3 4', '5 6', '7 8']
    result = run_script('matrix_mult.py', input_data).split('\n')
    assert result == ['19 22', '43 50']

def test_matrix_mult_3x3():
    input_data = ['3', '1 0 0', '0 1 0', '0 0 1', '1 2 3', '4 5 6', '7 8 9']
    result = run_script('matrix_mult.py', input_data).split('\n')
    assert result == ['1 2 3', '4 5 6', '7 8 9']

def test_matrix_mult_zeros():
    input_data = ['2', '0 0', '0 0', '1 2', '3 4']
    result = run_script('matrix_mult.py', input_data).split('\n')
    assert result == ['0 0', '0 0']

def test_matrix_mult_identity_left():
    input_data = ['2', '1 0', '0 1', '3 7', '2 5']
    result = run_script('matrix_mult.py', input_data).split('\n')
    assert result == ['3 7', '2 5']

def test_matrix_mult_negative():
    input_data = ['2', '1 -1', '-1 1', '1 1', '1 1']
    result = run_script('matrix_mult.py', input_data).split('\n')
    assert result == ['0 0', '0 0']