#
class Person(object):
    count = None

    @classmethod
    def setCount(cls, value):
        cls.count = value

    def getCountValue(self):
        print(Person.count)

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        print("Person.count = {}".format(Person.count))

    def __hash__(self):
        hashstr = self.name if self.name else ''
        hashstr = "{}{}".format(hashstr, self.age) if self.age else hashstr
        return hash(hashstr)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.name == other.name and self.age == other.age:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
