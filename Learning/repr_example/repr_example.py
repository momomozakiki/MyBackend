class PointWithoutRepr:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = PointWithoutRepr(3, 4)
print(p)        # Uses __str__ if defined, then __repr__, but we have neither -> default
print(repr(p))  # Explicitly call repr
print('\n')

class PointWithRepr:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"PointWithRepr({self.x}, {self.y})"

p = PointWithRepr(3, 4)
print(p)        # Now __str__ is not defined, so __repr__ is used
print(repr(p))  # Explicitly call repr
print('\n')

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        # This should look like a valid Python expression to recreate the object
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        # User-friendly string
        return f"({self.x}, {self.y})"

p = Point(3, 4)
print(p)          # Uses __str__: (3, 4)
print(repr(p))    # Uses __repr__: Point(3, 4)

# In a list, __repr__ is used for each element
points = [Point(1, 2), Point(3, 4)]
print(points)     # [Point(1, 2), Point(3, 4)]
print('\n')

class Student:
    def __init__(self, name, age, courses):
        self.name = name
        self.age = age
        self.courses = courses

    def __repr__(self):
        return f"Student(name={self.name!r}, age={self.age}, courses={self.courses!r})"

    def __str__(self):
        return f"Student {self.name}, {self.age} years old, taking {len(self.courses)} courses"

student = Student("Alice", 20, ["Math", "Physics"])
print(student)          # Student Alice, 20 years old, taking 2 courses
print(repr(student))    # Student(name='Alice', age=20, courses=['Math', 'Physics'])
print('\n')


# Example 2: Basic __repr__ Implementation

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"

    def __str__(self):
        return f"{self.name}: ${self.price} (x{self.quantity})"


# Create instance
p = Product("Laptop", 999.99, 10)

print(p)  # Laptop: $999.99 (x10)       (uses __str__)
print(repr(p))  # Product(name='Laptop', price=999.99, quantity=10)
print(str(p))  # Laptop: $999.99 (x10)

# In a list (always uses __repr__ for elements)
products = [p, Product("Phone", 499.99, 25)]
print(products)
# [Product(name='Laptop', price=999.99, quantity=10),
#  Product(name='Phone', price=499.99, quantity=25)]
print('\n')

# Example 3: Why __repr__ Should Allow Recreation
import copy

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        # This string can recreate the object!
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


v = Vector(3, 4)
print(repr(v))  # Vector(3, 4)

# You can actually recreate it!
repr_str = repr(v)  # "Vector(3, 4)"
recreated_v = eval(repr_str)  # Creates new Vector(3, 4)
print(recreated_v)  # (3, 4)
print(recreated_v == v)  # Might be True if we implement __eq__
print('\n')

# Example 4: Advanced - Proper Object Recreation
class Student:
    def __init__(self, name, age, courses=None):
        self.name = name
        self.age = age
        self.courses = courses if courses is not None else []

    def __repr__(self):
        # Handle edge cases properly
        courses_repr = repr(self.courses)  # Use repr for list
        return f"Student({self.name!r}, {self.age}, {courses_repr})"

    def __eq__(self, other):
        # For proper comparison
        return (self.name == other.name and
                self.age == other.age and
                self.courses == other.courses)


# Test
s1 = Student("Alice", 20, ["Math", "Physics"])
print(repr(s1))
# Student('Alice', 20, ['Math', 'Physics'])

# Recreate from repr
s2 = eval(repr(s1))
print(s2)  # Same as s1
print(s1 == s2)  # True (if __eq__ is defined)
print('\n')

# Example 5: What Happens in Containers
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    # Only __repr__, no __str__
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}')"


class BookWithBoth:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return f"BookWithBoth('{self.title}', '{self.author}')"

    def __str__(self):
        return f"{self.title} by {self.author}"


# Test
book1 = Book("1984", "Orwell")
book2 = BookWithBoth("Brave New World", "Huxley")

print(book1)  # Book('1984', 'Orwell') - uses __repr__ as fallback
print(book2)  # Brave New World by Huxley - uses __str__

# In a list (ALWAYS uses __repr__!)
library = [book1, book2]
print(library)
# [Book('1984', 'Orwell'), BookWithBoth('Brave New World', 'Huxley')]

print('\n')

# Example 6: Real-World Scenario - Database Models
class User:
    def __init__(self, user_id, username, email, is_active=True):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.is_active = is_active
        self.created_at = "2024-01-15"  # Normally from datetime

    def __repr__(self):
        # Include only essential fields for recreation
        return (f"User(user_id={self.user_id!r}, "
                f"username={self.username!r}, "
                f"email={self.email!r}, "
                f"is_active={self.is_active})")

    def __str__(self):
        return f"@{self.username} ({self.email})"

    def to_dict(self):
        # For JSON serialization
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active
        }


# Usage
users = [
    User(1, "john_doe", "john@example.com"),
    User(2, "jane_doe", "jane@example.com", False),
    User(3, "admin", "admin@example.com")
]

print(users[0])  # @john_doe (john@example.com)
print(repr(users[0]))  # User(user_id=1, username='john_doe', email='john@example.com', is_active=
print(users)
print(str(users))

# Debugging in console
# >> > users[1]
jane_doe = User(user_id=2, username='jane_doe', email='jane@example.com', is_active=False)
print(repr(jane_doe))
print('\n')

# Example 2: Proper Implementation

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        """For developers - shows how to recreate object"""
        return f"Person(name={self.name!r}, age={self.age})"

    def __str__(self):
        """For users - friendly display"""
        return f"Name: {self.name}, Age: {self.age}"


person = Person("Bob", 25)

print(str(person))  # Name: Bob, Age: 25       ← User-friendly
print(repr(person))  # Person(name='Bob', age=25) ← Developer-friendly
print(person)  # Name: Bob, Age:25         ← Uses __str__

# In a list (uses __repr__ for all elements!)
people = [Person("Alice", 30), Person("Charlie", 35)]
print(people)
# [Person(name='Alice', age=30), Person(name='Charlie', age=35)]
print('\n')

# Real-World Use Cases
class BankAccount:
    def __init__(self, account_number, balance, currency="USD"):
        self.account_number = account_number
        self.balance = balance
        self.currency = currency

    def __repr__(self):
        """For logs, debugging, and database storage"""
        return (f"BankAccount("
                f"account_number={self.account_number!r}, "
                f"balance={self.balance}, "
                f"currency={self.currency!r})")

    def __str__(self):
        """For bank statements and customer communication"""
        # Hide sensitive info from users!
        masked_account = "****" + str(self.account_number)[-4:]
        return (f"Account: {masked_account}\n"
                f"Balance: {self.currency} {self.balance:.2f}")


account = BankAccount("1234567890", 1500.75)

# ===== FOR CUSTOMER =====
print("Your Account Statement:")
print(str(account))
# Output:
# Your Account Statement:
# Account: ****7890
# Balance: USD 1500.75

# ===== FOR DEVELOPER =====
print("\nDebug View:")
print(repr(account))
# Output:
# BankAccount(account_number='1234567890', balance=1500.75, currency='USD')

print('\n')

# Edge Cases Where !r is Critical:

# 1. Strings with special characters
value = "line1\nline2\ttab"
print(f"Without !r: {value}")      # Shows actual newlines and tabs (messy)
print(f"With !r: {value!r}")        # 'line1\\nline2\\ttab' (escaped)
print('\n')
# 2. Decimal/Float precision
from decimal import Decimal
value = Decimal('1.234567890123456789')
print(f"Without !r: {value}")      # 1.234567890123456789
print(f"With !r: {value!r}")       # Decimal('1.234567890123456789')
# !r shows it's a Decimal, not a float
print('\n')
# 3. Custom objects
class Custom:
    def __str__(self):
        return "Custom via str"
    def __repr__(self):
        return "Custom via repr"

value = Custom()
print(f"Without !r: {value}")      # Custom via str
print(f"With !r: {value!r}")       # Custom via repr
# repr is more accurate for debugging
print('\n')
# 4. Tuples/Lists/Dicts
value = {"key": "value", "num": 42}
print(f"Without !r: {value}")      # {'key': 'value', 'num': 42}
print(f"With !r: {value!r}")       # {'key': 'value', 'num': 42}
# Actually same output for dicts, but safe for consistency