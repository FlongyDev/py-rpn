""" Обратная польская запись: калькулятор """
from typing import Callable

all_ops: dict[str, Callable[[list], int]] = {}


def binary_op(token: str) -> Callable[[Callable[[int, int], int]], Callable[[list], int]]:
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
        return redef
    return make_binop


# add = binary_op('+')(add)
@binary_op('+')
def add(a, b):
    return a + b


@binary_op('-')
def sub(a, b):
    return a - b


@binary_op('*')
def mul(a, b):
    return a * b


@binary_op('//')
def div(a, b):
    return a // b


@binary_op('%')
def mod(a, b):
    return a % b


@binary_op('^')
def power(a, b):
    return a ** b


# "3 4 +"
def execute_program(program: str) -> int:
    stack = []
    for token in program.split():
        operation = all_ops.get(token, None)
        if operation is not None:
            operation(stack)
        else:
            try:
                stack.append(int(token))
            except ValueError:
                raise ValueError(f"{token!r} - неизвестная операция или не целое число")

    if len(stack) != 1:
        raise ValueError(f"Ошибка! К концу вычислений на стаке осталось не одно число: {stack}")

    return stack.pop()


if __name__ == "__main__":
    print(execute_program("15 7 %"), "==", 1)
    print(execute_program("3 6 3 * 1 4 - 2 ^ // +"), "==", 5)
