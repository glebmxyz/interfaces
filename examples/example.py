from interfaces import Interface, implements


class ISampleInterface(Interface):
    name: str
    count: int
    def equals(self, a: str, b: str):
        return [a, b]


class ISampleExtends(ISampleInterface, Interface):
    def my_method(self, a, b, c):
        return a, b, c


class IOtherInterface(Interface):
    def other_method(self, book, article) -> int:
        pass


@implements(ISampleExtends, IOtherInterface)
class Implementation:
    name = 'Bob'
    count = 3

    def other_method(self, book, article) -> int:
        pass

    def equals(self, a: str, b: str):
        pass

    def my_method(self, a, b, c):
        pass


Implementation()
