from ensure import ensure_annotations
from dummypackage12624.custom_exception import InvalidUserInput


@ensure_annotations
def addition(x: int, y: int) -> int:
    return x + y


@ensure_annotations
def subtraction(x: int, y: int) -> int:
    if (x - y) < 0:
        raise InvalidUserInput("Input2 >> Input1")
    else:
        return x - y


@ensure_annotations
def division(x: int, y: int) -> float:
    try:
        return x / y
    except Exception:
        raise InvalidUserInput("Invalid user input")

# something ....