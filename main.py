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

all_ops: dict[TOKEN_TYPE, Callable[[list], int]] = {}
all_tokens: dict[str, TOKEN_TYPE] = {}


def binary_op(str_token: str, token: TOKEN_TYPE) -> Callable[[Callable[[int, int], int]], Callable[[list], int]]:
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
        return redef
    return make_binop


# add = binary_op('+')(add)
@binary_op('+', ADDITION)
def add(a, b):
    return a + b


@binary_op('-', SUBTRACTION)
def sub(a, b):
    return a - b


@binary_op('*', MULTIPLICATION)
def mul(a, b):
    return a * b


@binary_op('//', DIVISION)
def div(a, b):
    return a // b


@binary_op('%', MODULO)
def mod(a, b):
    return a % b


@binary_op('^', POWER)
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


def execute_program(program: list[tuple[TOKEN_TYPE]]) -> int:
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
    print(execute_program(parse_str_postfix("15 7 %")), "==", 1)
    print(execute_program(parse_str_postfix("3 6 3 * 1 4 - 2 ^ // +")), "==", 5)
