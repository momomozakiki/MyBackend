# 🚀 Python Dataclass Magic Methods Cheat Sheet

## 📋 **Dataclass Decorator Parameters**

```python
@dataclass(
    init=True,        # Generate __init__? (Default: True)
    repr=True,        # Generate __repr__? (Default: True)
    eq=True,          # Generate __eq__? (Default: True)
    order=False,      # Generate ordering methods? (Default: False)
    unsafe_hash=False,# Force __hash__ generation? (Default: False)
    frozen=False      # Make immutable? (Default: False)
)
class MyClass:
    # fields here
```

## 🧙 **Auto-Generated Magic Methods Table**

| Method | Generated When | Description | Example Output |
|--------|----------------|-------------|----------------|
| **`__init__`** | `init=True` (default) | Auto-initializes all fields | `MyClass(name='John', age=30)` |
| **`__repr__`** | `repr=True` (default) | Shows class name + all fields | `MyClass(name='John', age=30)` |
| **`__eq__`** | `eq=True` (default) | Compares all fields for equality | `obj1 == obj2` compares all fields |
| **`__hash__`** | When `frozen=True` OR `unsafe_hash=True` | Hash based on field values | Enables use in sets/dicts |
| **`__lt__`, `__le__`, `__gt__`, `__ge__`** | `order=True` | Field-by-field comparison | `obj1 < obj2` compares all fields |
| **`__setattr__`** | Never (but modified when `frozen=True`) | Prevents modification if frozen | Raises `FrozenInstanceError` |
| **`__delattr__`** | Never (but modified when `frozen=True`) | Prevents deletion if frozen | Raises `FrozenInstanceError` |

## 🔧 **Manual Magic Methods You Can Add**

| Method | Purpose | Example |
|--------|---------|---------|
| **`__post_init__`** | Validation/computation after init | Validate data, compute derived fields |
| **`__str__`** | User-friendly string representation | Pretty print format |
| **Custom `__repr__`** | Override auto-generated format | Hide sensitive data, custom format |
| **`@property`** | Computed properties | `@property def full_name(self):` |

## 📊 **Comparison: Dataclass vs Regular Class**

| Magic Method | Dataclass (Auto) | Regular Class (Manual) |
|--------------|------------------|------------------------|
| `__init__` | ✅ Auto-generated | ❌ Must write manually |
| `__repr__` | ✅ Shows all fields | ❌ Shows memory address |
| `__eq__` | ✅ Compares all fields | ❌ Compares by identity |
| `__hash__` | ✅ Auto with `frozen=True` | ❌ Must implement |
| `__str__` | ❌ Uses `__repr__` | ❌ Must implement |
| Ordering | ✅ With `order=True` | ❌ Must implement all 4 |

## 🎯 **Common Patterns & Examples**

### Basic Dataclass
```python
@dataclass
class Person:
    name: str
    age: int
    # Gets: __init__, __repr__, __eq__
```

### Immutable Dataclass
```python
@dataclass(frozen=True)
class Point:
    x: int
    y: int
    # Gets: __init__, __repr__, __eq__, __hash__
```

### Ordered Dataclass
```python
@dataclass(order=True)
class Product:
    name: str
    price: float
    # Gets: __init__, __repr__, __eq__, __lt__, __le__, __gt__, __ge__
```

### With Validation
```python
@dataclass
class Email:
    address: str
    
    def __post_init__(self):
        if '@' not in self.address:
            raise ValueError("Invalid email")
```

### Custom `__repr__`
```python
@dataclass
class Secret:
    username: str
    password: str  # Sensitive!
    
    def __repr__(self):
        return f"Secret(username={self.username!r}, password='***')"
```

## ⚡ **Quick Reference Card**

```python
# Import (Python 3.7+)
from dataclasses import dataclass, field
from typing import ClassVar, Optional

# Basic structure
@dataclass
class Example:
    # Regular field
    name: str
    
    # Field with default value
    age: int = 18
    
    # Field with factory function
    tags: list[str] = field(default_factory=list)
    
    # Class variable (NOT in __init__)
    count: ClassVar[int] = 0
    
    # Excluded from __repr__ and __eq__
    _internal: str = field(default="", repr=False, compare=False)
    
    def __post_init__(self):
        # Validation/computation
        pass
```

## 🔄 **Inheritance Behavior**

| Feature | Behavior |
|---------|----------|
| **Field Order** | Parent fields first, then child fields |
| **Default Values** | Fields with defaults must come after fields without |
| **Method Inheritance** | Child can override auto-generated methods |
| **Multiple Inheritance** | Supported but complex (use `@dataclass(repr=False)` on parents) |

## 🎨 **Field() Function Options**

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    # Basic default
    name: str = "default"
    
    # Factory function for mutable defaults
    items: list = field(default_factory=list)
    
    # Exclude from repr
    password: str = field(default="", repr=False)
    
    # Exclude from comparisons
    timestamp: float = field(default=0.0, compare=False)
    
    # Metadata (for documentation/libraries)
    description: str = field(
        default="", 
        metadata={"unit": "meters", "max": 100}
    )
```

## 🚫 **Common Pitfalls & Solutions**

| Problem | Solution |
|---------|----------|
| **Mutable default values** | Use `default_factory=list` instead of `=[]` |
| **Inheritance with defaults** | Reorder fields or use `@dataclass(repr=False)` on parent |
| **Frozen dataclass modification** | Use `object.__setattr__(self, 'field', value)` in `__post_init__` |
| **Custom `__init__` with dataclass** | Don't! Use `__post_init__` instead |

## 📈 **When to Use Dataclass**

✅ **Use dataclass when:**
- Simple data containers (DTOs, config objects)
- Need `__repr__`, `__eq__`, `__hash__` for free
- Want immutability (`frozen=True`)
- Reduce boilerplate code

❌ **Avoid dataclass when:**
- Complex business logic needed
- Inheritance hierarchies are complex
- Need tight control over memory layout
- Performance-critical code

## 💡 **Pro Tips**

1. **`from dataclasses import asdict, astuple`** - Convert to dict/tuple
2. **`from dataclasses import replace`** - Create modified copies (especially for `frozen=True`)
3. **Use `@dataclass(slots=True)` in Python 3.10+** for memory efficiency
4. **Combine with `typing.NamedTuple`** for hybrid behavior
5. **`dataclasses.is_dataclass(obj)`** - Check if something is a dataclass

---

## 📖 **Complete Example**

```python
from dataclasses import dataclass, field, asdict
from typing import ClassVar, Optional
from datetime import datetime

@dataclass(frozen=True, order=True)
class Transaction:
    # Auto-generated: __init__, __repr__, __eq__, __hash__, ordering methods
    amount: float
    currency: str = "USD"
    timestamp: datetime = field(default_factory=datetime.now)
    id: Optional[int] = field(default=None, compare=False)
    
    # Class variable (not in fields)
    transaction_count: ClassVar[int] = 0
    
    def __post_init__(self):
        # Validation
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
    
    @property
    def formatted(self):
        """Computed property"""
        return f"{self.currency} {self.amount:.2f}"
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)

# Usage
tx1 = Transaction(100.0, "USD")
tx2 = Transaction(200.0, "EUR")
print(repr(tx1))  # Transaction(amount=100.0, currency='USD', timestamp=...)
print(tx1 == tx2)  # False (auto __eq__)
print(tx1 < tx2)   # True (because order=True)
```

---

**Save this cheat sheet!** It covers 95% of what you need to know about dataclass magic methods. 🎉