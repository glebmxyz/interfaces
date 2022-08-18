import inspect

from typing import Tuple, Type


class InterfaceMeta(type):
    def __new__(mcs, name: str, bases: Tuple[Type, ...], dct: dict):
        def _inherits_from_interface(b: Tuple[Type, ...]) -> bool:
            return any(map(lambda x: x.__name__ == 'Interface' and x.__module__ == name, b))

        if _inherits_from_interface(bases) and len(bases) > 1:
            raise Exception("If present, 'Interface' class must be the only base of an interface.")

        for base in bases:
            if not issubclass(base, Interface):
                raise Exception(f"{base} is not an interface. "
                                "All interface's bases must be subclasses of Interface type.")

        return super().__new__(mcs, name, bases, dct)


class Interface(metaclass=InterfaceMeta):
    def __new__(cls) -> None:
        raise Exception('Cannot create an instance of an interface.')


def implements(*args: [Type, ...]):
    def inner(cls: Type):
        methods_to_implement = {}

        class CombinedInterface(*args):
            pass

        # Skip 'object' and 'Interface'
        for interface in tuple(reversed(CombinedInterface.__mro__))[2:]:
            # TODO: Add properties
            for key, value in interface.__dict__.items():
                if key in ('__module__', '__doc__') or not callable(value):
                    continue
                methods_to_implement[key] = inspect.getfullargspec(value)

        for method_name, arg_spec in methods_to_implement.items():
            # TODO: Useful error message
            method = getattr(cls, method_name)

            # TODO: Check if callable
            if inspect.getfullargspec(method) != arg_spec:
                # TODO: Detailed error message
                raise Exception(f"{method_name}'s arg_spec doesn't match desired")

        return cls

    return inner
