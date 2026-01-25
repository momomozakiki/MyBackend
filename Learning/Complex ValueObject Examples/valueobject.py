from dataclasses import dataclass

@dataclass(frozen=True)
class ValueObject:
    print(f'Value Object is called')
    def __eq__(self, other):
        print('eq is called')
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value

    def __hash__(self):
        print('hash is called')
        return hash(self.value)

    def __repr__(self):
        print('repr is called')
        """
        Universal __repr__ that works for most ValueObjects
        Can be overridden for special cases
        """
        import dataclasses

        if dataclasses.is_dataclass(self):
            field_values = []
            for field in dataclasses.fields(self):
                value = getattr(self, field.name)
                field_values.append(f"{field.name}={value!r}")
            args = ', '.join(field_values)
            print('dataclass : ' + args)
        else:
            # Fallback for non-dataclass objects
            attrs = []
            for attr_name in dir(self):
                if not attr_name.startswith('_') and hasattr(self, attr_name):
                    attr_value = getattr(self, attr_name)
                    if not callable(attr_value):
                        attrs.append(f"{attr_name}={attr_value!r}")
            args = ', '.join(attrs)
            print('dataclass : ' + args)

        return f"{self.__class__.__name__}({args})"

