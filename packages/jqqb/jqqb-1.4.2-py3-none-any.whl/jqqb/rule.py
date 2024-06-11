from datetime import datetime

from pytimeparse.timeparse import timeparse

from jqqb.operators import Operators


BOOLEAN_VALUES = (
    "true",
    "1",
    "t",
    "y",
    "yes",
    "yeah",
    "yup",
    "certainly",
    "uh-huh",
    "oui",
    "o",
)


class Rule:
    def __init__(self, rule_dict):
        self.id = rule_dict["id"]
        self.field = rule_dict["field"]
        self.type = rule_dict["type"]
        self.input = rule_dict["input"]
        self.operator = rule_dict["operator"]
        self.value = rule_dict["value"]
        self.value_type = rule_dict["value_type"]

    def evaluate(self, obj):
        results = []
        result = self.get_operator()(
            self.get_input(obj, results), self.get_value()
        )
        return result

    def inputs(self, obj):
        results = []
        inputs = self.get_input(obj, results)
        return inputs

    def values(self):
        values = self.get_value()
        return values

    def inspect(self, obj):
        return self.inputs(obj), self.values(), self.evaluate(obj)

    def get_operator(self):
        return getattr(Operators, "eval_" + self.operator)

    def get_input(self, obj, results):
        fields = self.field.split(".")
        fd_index = 0

        if isinstance(obj, list):
            for i in range(len(obj)):
                self.get_input(obj[i], results)

        elif isinstance(obj, dict):
            while fd_index < len(fields) and fields[fd_index] not in obj:
                fd_index += 1

            if fd_index < len(fields) and fields[fd_index] in obj:
                self.get_input(obj[fields[fd_index]], results)

        else:
            results.append(self.typecast_value(obj, type=self.type))

        results = [x for x in results if x is not None] or None
        return results

    def get_value(self):
        if isinstance(self.value, list):
            return list(
                map(
                    lambda x: self.typecast_value(x, type=self.value_type),
                    self.value,
                )
            )
        return self.typecast_value(self.value, type=self.value_type)

    @staticmethod
    def typecast_value(value_to_cast, type):
        if value_to_cast is None:
            return None

        if type == "string":
            return str(value_to_cast)
        elif type == "integer":
            return int(value_to_cast)
        elif type == "double":
            return float(value_to_cast)
        elif type == "boolean":
            if isinstance(value_to_cast, str):
                return value_to_cast.lower() in BOOLEAN_VALUES
        elif type == "list":
            ...
        elif type == "datetime":
            return (
                datetime.fromisoformat(value_to_cast)
                if (isinstance(value_to_cast, str) and value_to_cast != "")
                else value_to_cast
            )
        elif type == "date":
            return (
                datetime.strptime(value_to_cast, "%Y-%m-%d")
                if (isinstance(value_to_cast, str) and value_to_cast != "")
                else value_to_cast
            )
        elif type == "time":
            return (
                timeparse(value_to_cast)
                if (isinstance(value_to_cast, str) and value_to_cast != "")
                else value_to_cast
            )
        return value_to_cast
