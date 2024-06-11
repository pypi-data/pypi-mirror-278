from . import utils


class Operators:

    # left = The property of the object being evaluated.
    # right = The value that was entered/selected by the user
    # from the frontend (rule `value` property)

    @staticmethod
    def eval_begins_with(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x.startswith(right), left))
        return False

    @staticmethod
    def eval_between(inputs, bounds):
        if isinstance(inputs, list):
            return any(map(lambda x: bounds[0] < x < bounds[1], inputs))
        return False

    @staticmethod
    def eval_contains(left, right):
        if isinstance(left, list):
            if isinstance(right, list):
                return any([any(map(lambda x: r in x, left)) for r in right])
            return any([right in l for l in left])
        return False

    @staticmethod
    def eval_ends_with(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x.endswith(right), left))
        return False

    @staticmethod
    def eval_equal(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x == right, left))
        return False

    @staticmethod
    def eval_greater(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x > right, left))
        return False

    @staticmethod
    def eval_greater_or_equal(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x >= right, left))
        return False

    @staticmethod
    def eval_in(left, right):
        if isinstance(left, list):
            return all([_ in right for _ in left])
        return False

    @staticmethod
    def eval_is_empty(inputs, _):
        if isinstance(inputs, list):
            return not any(map(lambda x: bool(x), inputs))
        return False

    @staticmethod
    def eval_is_not_empty(inputs, _):
        if isinstance(inputs, list):
            return any(map(lambda x: bool(x), inputs))
        return False

    @staticmethod
    def eval_is_not_null(inputs, _):
        if isinstance(inputs, list):
            return any(map(lambda x: x is not None, inputs))
        return False

    @staticmethod
    def eval_is_null(inputs, _):
        if isinstance(inputs, list):
            return not any(map(lambda x: x is not None, inputs))
        return True

    @staticmethod
    def eval_less(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x < right, left))
        return False

    @staticmethod
    def eval_less_or_equal(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x <= right, left))
        return False

    @staticmethod
    def eval_not_begins_with(left, right):
        if isinstance(left, list):
            return not any(map(lambda x: x.startswith(right), left))
        return False

    @staticmethod
    def eval_not_between(inputs, bounds):
        if isinstance(inputs, list):
            return not any(map(lambda x: bounds[0] < x < bounds[1], inputs))
        return False

    @staticmethod
    def eval_not_contains(left, right):
        if isinstance(left, list):
            if isinstance(right, list):
                return not any(
                    [any(map(lambda x: r in x, left)) for r in right]
                )
            return not any([right in l for l in left])
        return False

    @staticmethod
    def eval_not_ends_with(left, right):
        if isinstance(left, list):
            return not any(map(lambda x: x.endswith(right), left))
        return False

    @staticmethod
    def eval_not_equal(left, right):
        if isinstance(left, list):
            return not any(map(lambda x: x == right, left))
        return False

    @staticmethod
    def eval_not_in(left, right):
        if isinstance(left, list):
            return not all([_ in right for _ in left])
        return False

    @staticmethod
    def eval_length_equal(left, right):
        if isinstance(left, list):
            length = len(right) if isinstance(right, list) else int(right)
            return len(left) == length
        return False

    @staticmethod
    def eval_length_not_equal(left, right):
        if isinstance(left, list):
            length = len(right) if isinstance(right, list) else int(right)
            return len(left) != length
        return False

    @staticmethod
    def eval_length_greater(left, right):
        if isinstance(left, list):
            length = len(right) if isinstance(right, list) else int(right)
            return len(left) > length
        return False

    @staticmethod
    def eval_length_greater_or_equal(left, right):
        if isinstance(left, list):
            length = len(right) if isinstance(right, list) else int(right)
            return len(left) >= length
        return False

    @staticmethod
    def eval_length_less(left, right):
        if isinstance(left, list):
            length = len(right) if isinstance(right, list) else int(right)
            return len(left) < length
        return False

    @staticmethod
    def eval_length_less_or_equal(left, right):
        if isinstance(left, list):
            length = len(right) if isinstance(right, list) else int(right)
            return len(left) <= length
        return False

    @staticmethod
    def eval_occurrence(left, right):
        """

        This funtion compares the number of occurrences of a value with an
        integer value and returns a boolean indicating whether the condition
        is true or false

        Args:
            left (list): list of values extracted from the inputs object.
            right (str): string that represents the condition that we want to
                check about the occurences. It must match this pattern:
                <value> <operator> <int>

        Returns:
            bool: a boolean value whether the condition is true or false
        """
        if isinstance(left, list):
            if utils.validate_string(right):
                (
                    left_operand,
                    operator,
                    right_operand,
                ) = utils.split_string_by_operator(right)
                occurence = left.count(left_operand)
                return operator(occurence, right_operand)
            return False
        return False
