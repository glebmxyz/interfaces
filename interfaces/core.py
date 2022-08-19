import inspect

from typing import Tuple, Type


class InterfaceMeta(type):
    def __new__(mcs, name: str, bases: Tuple[Type, ...], dct: dict):
        for key, value in dct.items():
            if key in ('__module__', '__qualname__', '__annotations__'):
                continue

            if not callable(value):
                raise Exception(f"'{key}': Only methods and annotations can be declared in an interface.")

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
        methods = {}
        annotations = {}

        class CombinedInterface(*args):
            pass

        # Skip 'object' and 'Interface'
        for interface in tuple(reversed(CombinedInterface.__mro__))[2:]:
            annotations |= interface.__annotations__
            for key, value in interface.__dict__.items():
                if key in ('__module__', '__doc__', '__annotations__'):
                    continue
                methods[key] = inspect.getfullargspec(value)

        for key, annotation in annotations.items():
            prop = getattr(cls, key)

            # TODO: Generic types
            if not isinstance(prop, annotation):
                raise Exception(f"'{prop}' must be an instance of {annotation}.")

        for method_name, arg_spec in methods.items():
            # TODO: Useful error message
            method = getattr(cls, method_name)

            if not callable(method):
                raise Exception(f"'{method_name}' must be a method.")

            if inspect.getfullargspec(method) != arg_spec:
                # TODO: Detailed error message
                raise Exception(f"{method_name}'s arg_spec doesn't match desired")

        return cls

    return inner
