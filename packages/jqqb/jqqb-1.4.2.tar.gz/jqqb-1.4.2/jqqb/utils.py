import operator
import re

from decimal import Decimal


def validate_string(input_string):
    pattern = (
        r"^\s*([^{}\s]+(\s+[^{}\s]+)*)\s+([><]=?|=)\s*([+-]?\d+(\.\d+)?)\s*$"
    )
    match = re.match(pattern, input_string)
    return bool(match)


def split_string_by_operator(input_string):
    operators = {
        ">=": operator.ge,
        ">": operator.gt,
        "<=": operator.le,
        "<": operator.lt,
        "=": operator.eq,
    }

    for op in operators.keys():
        pattern = re.escape(op)
        parts = re.split(pattern, input_string)

        if len(parts) == 2:
            left, right = map(str.strip, parts)
            return left, operators[op], Decimal(right)

    # If no operator is found
    return None, None, None
