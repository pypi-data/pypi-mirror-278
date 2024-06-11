"""
    Any of the values contains collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AnyContains(CollectionCondition):
    """
        Condition for any value of `what` in `values`
    """

    def _is_satisfied(self) -> bool:
        for i in self.values:
            for w in self.what:
                if self.value_is_none(i) and self.value_is_none(w):
                    return True
                elif not self.is_string(i) or not self.is_string(w):
                    continue

                if i in w:
                    return True
        return False


class AnyContainsSchema(CollectionConditionSchema):
    """
        JSON schema for any in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return AnyContains(**data)
