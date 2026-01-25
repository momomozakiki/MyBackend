from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    def __eq__(self, other):
        print(f"Comparing: {self.__class__.__name__} vs {other.__class__.__name__}")
        print(f"isinstance({other.__class__.__name__}, {self.__class__.__name__}): {isinstance(other, self.__class__)}")

        if not isinstance(other, self.__class__):
            return False
        # For Email/Money with single value field
        if hasattr(self, 'value'):
            return self.value == other.value
        # For Money with multiple fields
        if hasattr(self, 'amount') and hasattr(self, 'currency'):
            return self.amount == other.amount and self.currency == other.currency
        return False

    def __hash__(self):
        if hasattr(self, 'value'):
            return hash(self.value)
        if hasattr(self, 'amount') and hasattr(self, 'currency'):
            return hash((self.amount, self.currency))
        return id(self)


@dataclass(frozen=True)
class Email(ValueObject):
    value: str


@dataclass(frozen=True)
class UserId(ValueObject):
    value: str


@dataclass(frozen=True)
class Money(ValueObject):
    amount: float
    currency: str


# Usage
email1 = Email("john@example.com")
email2 = Email("john@example.com")
email3 = Email("jane@example.com")

print(email1 == email2)  # True (same type, same value)
print(email1 == email3)  # False (same type, different value)

user1 = UserId("123")
user2 = UserId("123")
print(user1 == user2)  # True (same type, same value)

print(email1 == user1)  # False (different types!)

# Can use in sets and dictionaries
email_set = {email1, email2, email3}  # {Email("john@example.com"), Email("jane@example.com")}
print(f"Set size: {len(email_set)}")  # 2 (not 3, because email1 == email2)