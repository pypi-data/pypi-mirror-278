import json
from jqqb.rule_group import RuleGroup


class QueryBuilder:
    def __init__(self, rule_set):
        if isinstance(rule_set, str):
            self.parsed_rule_set = json.loads(rule_set)
        else:
            self.parsed_rule_set = rule_set

    def match_objects(self, objects):
        return list(filter(lambda x: self.object_matches_rules(x), objects))

    def object_matches_rules(self, obj):
        return RuleGroup(self.parsed_rule_set).evaluate(obj)

    def inspect_objects(self, objects):
        return [
            {
                "object": obj,
                "rules": self.parsed_rule_set,
                "selected": self.object_matches_rules(obj),
                "results": self.object_results_inspection(obj),
            }
            for obj in objects
        ]

    def object_results_inspection(self, obj):
        return RuleGroup(self.parsed_rule_set).inspect(obj)
