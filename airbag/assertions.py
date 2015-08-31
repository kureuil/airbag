__author__ = 'person_l'


class AssertionFactory:
    registry = {}

    @classmethod
    def register(cls, assertion_cls, assertion_type):
        cls.registry[assertion_type] = assertion_cls

    @classmethod
    def make(cls, assertion_name, value):
        return cls.registry[assertion_name](value=value)


def assertion(assertion_type):
    def assertion_register(assertion_cls):
        AssertionFactory.register(assertion_cls, assertion_type)
        return assertion_cls
    return assertion_register


class Assertion:
    def __init__(self, value):
        super().__init__()
        self.value = value

    def check(self, user_value):
        return False


@assertion('is')
class IsAssertion(Assertion):
    def check(self, user_value):
        return self.value == user_value


@assertion('not')
class NotAssertion(Assertion):
    def check(self, user_value):
        return self.value != user_value


@assertion('in')
class InAssertion(Assertion):
    def check(self, user_value):
        return user_value in self.value


@assertion('notin')
class NotInAssertion(Assertion):
    def check(self, user_value):
        return user_value not in self.value


@assertion('startswith')
class StartsWithAssertion(Assertion):
    def check(self, user_value):
        return self.value.startswith(user_value)


@assertion('endswith')
class EndsWithAssertion(Assertion):
    def check(self, user_value):
        return self.value.endswith(user_value)
