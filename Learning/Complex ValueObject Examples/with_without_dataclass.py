from dataclasses import dataclass

@dataclass(frozen=True)
class ValueObject:
    print('Value Object is called')
    def __repr__(self):
        return "ValueObject's custom repr"

# Regular class inheriting from ValueObject
class RegularClass(ValueObject):
    def __init__(self, x):
        self.x = x

# Dataclass inheriting from ValueObject
@dataclass(frozen=True)
class DataClass(ValueObject):
    x: int
    # y: str

# Test
regular = RegularClass(10)
dataclass_obj = DataClass(10)

print('without dataclass : ' + repr(regular))      # Output: ValueObject's custom repr
print('with dataclass : ' +  repr(dataclass_obj)) # Output: DataClass(x=10) - NOT ValueObject's custom repr!