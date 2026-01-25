class DemoMagic:
    def __init__(self, value):
        """Called when object is created"""
        self.value = value
        print(f"Created object with value: {value}")

    def __eq__(self, other):
        """Called when using =="""
        print("Using ==")
        return self.value == other.value

    def __hash__(self):
        """Called when using hash() or putting in set/dict"""
        print("Computing hash")
        return hash(self.value)

    def __str__(self):
        """Called when using str() or print()"""
        print("Converting to string")
        return f"Demo({self.value})"

    def __repr__(self):
        """Called in debugger or repr()"""
        print("Getting detailed representation")
        return f"DemoMagic({self.value!r})"

    def __len__(self):
        """Called when using len()"""
        print("Getting length")
        return len(str(self.value))

    def __add__(self, other):
        """Called when using +"""
        print("Adding objects")
        return DemoMagic(self.value + other.value)


# Usage
obj = DemoMagic("test")  # __init__ called
print(obj == obj)  # __eq__ called
print(hash(obj))  # __hash__ called
print(str(obj))  # __str__ called
print(len(obj))  # __len__ called
print(obj + obj)  # __add__ called