""" Обратная польская запись: калькулятор """
from typing import Callable

TOKEN_TYPE = int
INTERMEDIATE = list[tuple[TOKEN_TYPE]]

# Enum
PUSH = 0
ADDITION = 1
SUBTRACTION = 2
MULTIPLICATION = 3
DIVISION = 4
MODULO = 5
POWER = 6
OPEN_BRACKET = 7

all_ops: dict[TOKEN_TYPE, Callable[[list], int]] = {}
all_tokens: dict[str, TOKEN_TYPE] = {}
all_priorities: dict[TOKEN_TYPE, int] = {}


def binary_op(str_token: str, token: TOKEN_TYPE, priority: int) -> Callable[[Callable[[int, int], int]], Callable[[list], int]]:
    def make_binop(func: Callable[[int, int], int]) -> Callable[[list], int]:
        def redef(stack: list) -> int:
            if len(stack) < 2:
                raise ValueError(f"Недостаточно операндов на стаке: len = {len(stack)}")

            b = stack.pop()
            a = stack.pop()
            result = func(a, b)

            stack.append(result)

            return result
        all_ops[token] = redef
        all_tokens[str_token] = token
        all_priorities[token] = priority
        return redef
    return make_binop


# add = binary_op('+')(add)
@binary_op('+', ADDITION, 0)
def add(a, b):
    return a + b


@binary_op('-', SUBTRACTION, 0)
def sub(a, b):
    return a - b


@binary_op('*', MULTIPLICATION, 1)
def mul(a, b):
    return a * b


@binary_op('//', DIVISION, 1)
def div(a, b):
    return a // b


@binary_op('%', MODULO, 1)
def mod(a, b):
    return a % b


@binary_op('^', POWER, 2)
def power(a, b):
    return a ** b


def parse_str_postfix(rpn: str) -> INTERMEDIATE:
    token_list = []
    for str_token in rpn.split():
        token = all_tokens.get(str_token, None)
        if token is not None:
            token_list.append((token,))
        else:
            try:
                value = int(str_token)
                token_list.append((PUSH, value))
            except ValueError:
                raise ValueError(f"{str_token!r} - неизвестная операция или не целое число")

    return token_list


def parse_str_infix(infix: str) -> INTERMEDIATE:
    token_list = []

    stack = []

    token = ""
    last_was_digit = False

    def process_op():
        nonlocal token
        if not token:
            return

        op1 = all_tokens.get(token, None)
        if op1 is None:
            raise ValueError(f"{token!r} - неизвестная операция")

        priority_op1 = all_priorities[op1]

        while len(stack) >= 1 and stack[-1] != OPEN_BRACKET and all_priorities[stack[-1]] >= priority_op1:
            token_list.append((stack.pop(),))

        stack.append(op1)

        token = ""

    def process_num():
        nonlocal token
        if not token:
            return

        value = int(token)
        token_list.append((PUSH, value))

        token = ""

    for ch in infix:
        if ch.isspace():
            continue

        if ch == "(":
            process_op()
            stack.append(OPEN_BRACKET)
        elif ch == ")":
            process_num()
            while len(stack) >= 1:
                # TODO: Не рассмотрены функции
                if (op := stack.pop()) != OPEN_BRACKET:
                    token_list.append((op,))
                else:
                    break
            else:
                raise ValueError("В выражении пропущена открывающая скобка")
        else:
            if ch.isdigit():
                if not last_was_digit:
                    process_op()

                last_was_digit = True
            else:
                if last_was_digit:
                    process_num()

                last_was_digit = False
            token += ch
    else:
        if token:
            if last_was_digit:
                process_num()
            else:
                raise ValueError("Неверная инфиксная запись (оканчивается на оператор)")

        for op in reversed(stack):
            if op == OPEN_BRACKET:
                raise ValueError("В выражении пропущена закрывающая скобка")
            token_list.append((op,))

    return token_list


def execute_program(program: INTERMEDIATE) -> int:
    stack = []
    for op in program:
        token = op[0]
        if token == PUSH:
            stack.append(op[1])
            continue

        func = all_ops.get(token, None)
        if func is None:
            raise ValueError(f"Операция {token} не реализована!")

        func(stack)

    if len(stack) != 1:
        raise ValueError(f"Ошибка! К концу вычислений на стаке осталось не одно число: {stack}")

    return stack.pop()


if __name__ == "__main__":
    print("Постфиксная запись")
    print(execute_program(parse_str_postfix("15 7 %")), "==", 1)
    print(execute_program(parse_str_postfix("3 6 3 * 1 4 - 2 ^ // +")), "==", 5)

    print("Инфиксная запись")
    print(execute_program(parse_str_infix("42 + 27")), "==", 69)
    print(execute_program(parse_str_infix("(4 + 5) * 2")), "==", 18)
