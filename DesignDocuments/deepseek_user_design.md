# 🗺️ **Advanced User Domain Design: Complete Roadmap & Implementation**

## 📋 **Design Philosophy**
- **Single Responsibility**: Each class handles one concern
- **Loose Coupling**: Classes communicate through IDs/interfaces, not direct dependencies
- **Immutable Value Objects**: All domain objects are immutable
- **Rich Domain Model**: Business logic in domain classes, not services
- **DDD Principles**: Aggregates, Entities, Value Objects, Repositories

---

## 🏗️ **System Architecture Roadmap**

### **Phase 1: Core Domain Models (Pure Classes)**
```
📁 domain/
├── 📁 value_objects/
│   ├── UserId.py
│   ├── EmailAddress.py
│   ├── PhoneNumber.py
│   ├── Address.py
│   └── ContactType.py
├── 📁 entities/
│   ├── User.py
│   ├── UserEmail.py
│   ├── UserPhone.py
│   ├── UserAddress.py
│   └── UserProfile.py
├── 📁 aggregates/
│   └── UserAggregate.py
└── 📁 repositories/
    ├── interfaces/
    └── specifications/
```

### **Phase 2: Application Layer**
```
📁 application/
├── 📁 use_cases/
│   ├── RegisterUser.py
│   ├── UpdateEmail.py
│   ├── ManageAddress.py
│   └── ManagePhone.py
└── 📁 services/
    ├── EmailService.py
    └── ValidationService.py
```

### **Phase 3: Infrastructure Layer**
```
📁 infrastructure/
├── 📁 persistence/
│   ├── models/          # SQLAlchemy models
│   │   ├── UserModel.py
│   │   ├── UserEmailModel.py
│   │   └── UserAddressModel.py
│   └── repositories/    # Concrete repository implementations
└── 📁 external/
    └── EmailProvider.py
```

---

## 💡 **Core Design Concepts**

### **1. Value Objects (Immutable, Validated)**
- No identity, defined by their attributes
- Immutable (frozen=True)
- Self-validating (__post_init__)
- Can be shared between entities

### **2. Entities (Mutable, Have Identity)**
- Defined by their identity (ID)
- Can change state over time
- Root entities manage their aggregate boundaries

### **3. Aggregates (Consistency Boundaries)**
- User is the aggregate root
- Manages consistency of emails, addresses, phones
- All changes go through the aggregate root

---

## 🛠️ **Implementation Code**

### **📁 1. Value Objects**

```python
# 📄 domain/value_objects/UserId.py
from dataclasses import dataclass
import uuid

@dataclass(frozen=True)
class UserId:
    """User ID value object - ensures unique identity"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("User ID cannot be empty")
        # Validate UUID format if using UUIDs
        try:
            uuid.UUID(self.value)
        except ValueError:
            raise ValueError("Invalid User ID format")
    
    @classmethod
    def generate(cls) -> 'UserId':
        """Factory method to generate new UserId"""
        return cls(str(uuid.uuid4()))

# 📄 domain/value_objects/EmailAddress.py
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class EmailAddress:
    """Email address value object with validation"""
    value: str
    provider: str = None  # Can be derived from domain
    
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Email cannot be empty")
        if not self.EMAIL_REGEX.match(self.value):
            raise ValueError(f"Invalid email format: {self.value}")
        
        # Auto-determine provider if not specified
        if self.provider is None:
            domain = self.value.split('@')[1]
            object.__setattr__(self, 'provider', self._get_provider(domain))
    
    def _get_provider(self, domain: str) -> str:
        """Extract provider from domain"""
        providers = {
            'gmail.com': 'Google',
            'outlook.com': 'Microsoft',
            'yahoo.com': 'Yahoo',
            'icloud.com': 'Apple'
        }
        return providers.get(domain, 'Custom')
    
    def is_same_provider(self, other: 'EmailAddress') -> bool:
        """Check if two emails are from same provider"""
        return self.provider == other.provider

# 📄 domain/value_objects/ContactType.py
from enum import Enum
from dataclasses import dataclass

class ContactType(Enum):
    """Types of contact information"""
    HOME = "home"
    WORK = "work"
    MOBILE = "mobile"
    BILLING = "billing"
    SHIPPING = "shipping"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    EMERGENCY = "emergency"
    OTHER = "other"

@dataclass(frozen=True)
class ContactTypeVO:
    """Contact Type as Value Object with validation"""
    value: ContactType
    
    def __post_init__(self):
        if not isinstance(self.value, ContactType):
            raise ValueError("Must be a valid ContactType enum")

# 📄 domain/value_objects/PhoneNumber.py
from dataclasses import dataclass
import re
from typing import Optional

@dataclass(frozen=True)
class PhoneNumber:
    """Phone number value object with international support"""
    value: str
    country_code: Optional[str] = None
    formatted_value: Optional[str] = None
    
    def __post_init__(self):
        # Remove all non-digit characters for validation
        digits = ''.join(filter(str.isdigit, self.value))
        
        if len(digits) < 10:
            raise ValueError("Phone number must have at least 10 digits")
        
        # Auto-detect country code if not provided
        if self.country_code is None:
            object.__setattr__(self, 'country_code', self._detect_country_code(digits))
        
        # Format the number
        if self.formatted_value is None:
            object.__setattr__(self, 'formatted_value', self._format_number(digits))
    
    def _detect_country_code(self, digits: str) -> str:
        """Auto-detect country code based on patterns"""
        if digits.startswith('1') and len(digits) == 11:
            return '+1'  # US/Canada
        elif digits.startswith('44'):
            return '+44'  # UK
        elif digits.startswith('61'):
            return '+61'  # Australia
        else:
            return '+??'  # Unknown
    
    def _format_number(self, digits: str) -> str:
        """Format phone number based on country code"""
        if self.country_code == '+1' and len(digits) == 11:
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        elif self.country_code == '+44':
            return f"{digits[:4]} {digits[4:7]} {digits[7:]}"
        return digits

# 📄 domain/value_objects/Address.py
from dataclasses import dataclass
from typing import Optional
from .ContactType import ContactType

@dataclass(frozen=True)
class Address:
    """Complete address value object"""
    street_line1: str
    street_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "USA"
    
    def __post_init__(self):
        if not self.street_line1:
            raise ValueError("Street address is required")
        if not self.city:
            raise ValueError("City is required")
        if not self.postal_code:
            raise ValueError("Postal code is required")
        
        # Validate postal code format
        if self.country == "USA":
            us_zip_regex = r'^\d{5}(?:[-\s]\d{4})?$'
            if not re.match(us_zip_regex, self.postal_code):
                raise ValueError("Invalid US ZIP code format")
    
    def get_full_address(self) -> str:
        """Get formatted full address"""
        lines = [self.street_line1]
        if self.street_line2:
            lines.append(self.street_line2)
        lines.extend([
            f"{self.city}, {self.state} {self.postal_code}",
            self.country
        ])
        return "\n".join(lines)
```

### **📁 2. Entities**

```python
# 📄 domain/entities/UserEmail.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from ..value_objects import EmailAddress, ContactType

@dataclass(frozen=True)
class UserEmail:
    """Entity linking User to Email with metadata"""
    user_id: str
    email: EmailAddress
    contact_type: ContactType = ContactType.PRIMARY
    is_verified: bool = False
    is_default: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    verified_at: Optional[datetime] = None
    
    def __post_init__(self):
        # Business rule: Default email must be primary
        if self.is_default and self.contact_type != ContactType.PRIMARY:
            raise ValueError("Default email must be PRIMARY contact type")
    
    def mark_as_verified(self) -> 'UserEmail':
        """Create new instance with verified status"""
        from dataclasses import replace
        return replace(
            self,
            is_verified=True,
            verified_at=datetime.now()
        )
    
    def set_as_default(self) -> 'UserEmail':
        """Create new instance as default email"""
        from dataclasses import replace
        return replace(
            self,
            is_default=True,
            contact_type=ContactType.PRIMARY
        )

# 📄 domain/entities/UserPhone.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from ..value_objects import PhoneNumber, ContactType

@dataclass(frozen=True)
class UserPhone:
    """Entity linking User to Phone with metadata"""
    user_id: str
    phone: PhoneNumber
    contact_type: ContactType = ContactType.MOBILE
    is_verified: bool = False
    is_default: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    verified_at: Optional[datetime] = None

# 📄 domain/entities/UserAddress.py
from dataclasses import dataclass, field
from datetime import datetime
from ..value_objects import Address, ContactType

@dataclass(frozen=True)
class UserAddress:
    """Entity linking User to Address with metadata"""
    user_id: str
    address: Address
    contact_type: ContactType = ContactType.HOME
    is_default: bool = False
    created_at: datetime = field(default_factory=datetime.now)

# 📄 domain/entities/UserProfile.py
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from ..value_objects import UserId

@dataclass(frozen=True)
class UserProfile:
    """User profile entity - separate from authentication"""
    user_id: UserId
    first_name: str
    last_name: str
    display_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    preferred_language: str = "en"
    timezone: str = "UTC"
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.display_name:
            object.__setattr__(self, 'display_name', f"{self.first_name} {self.last_name}")
        
        # Validate date of birth
        if self.date_of_birth:
            age = (date.today() - self.date_of_birth).days // 365
            if age < 13:
                raise ValueError("User must be at least 13 years old")
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> Optional[int]:
        """Calculate age from date of birth"""
        if not self.date_of_birth:
            return None
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

# 📄 domain/entities/User.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Set
from enum import Enum
from ..value_objects import UserId

class UserStatus(Enum):
    """User account status"""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"
    DELETED = "deleted"

class UserRole(Enum):
    """User roles"""
    GUEST = "guest"
    USER = "user"
    PREMIUM = "premium"
    MODERATOR = "moderator"
    ADMIN = "admin"

@dataclass(frozen=True)
class User:
    """
    Pure User entity - Only contains user-specific data
    No direct references to emails, addresses, phones
    These are managed through separate entities
    """
    id: UserId
    username: str
    password_hash: str  # Never store plain passwords!
    status: UserStatus = UserStatus.PENDING
    roles: Set[UserRole] = field(default_factory=lambda: {UserRole.USER})
    
    # Authentication & Security
    email_verified: bool = False
    phone_verified: bool = False
    two_factor_enabled: bool = False
    failed_login_attempts: int = 0
    account_locked_until: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_login_at: Optional[datetime] = None
    password_changed_at: datetime = field(default_factory=datetime.now)
    
    # Preferences (could be moved to separate entity)
    preferences: dict = field(default_factory=lambda: {
        "email_notifications": True,
        "sms_notifications": False,
        "newsletter": True,
        "theme": "light",
        "language": "en"
    })
    
    def __post_init__(self):
        """Business validation rules"""
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(self.roles) == 0:
            raise ValueError("User must have at least one role")
    
    # ========== Business Methods ==========
    
    @property
    def is_active(self) -> bool:
        """Check if user can log in"""
        return (self.status == UserStatus.ACTIVE and 
                self.email_verified and
                not self.is_locked)
    
    @property
    def is_locked(self) -> bool:
        """Check if account is locked"""
        if self.account_locked_until:
            return self.account_locked_until > datetime.now()
        return False
    
    def has_role(self, role: UserRole) -> bool:
        """Check if user has specific role"""
        return role in self.roles
    
    def can_login(self) -> bool:
        """Check if user is allowed to login"""
        return self.is_active and not self.is_locked
    
    # ========== State Change Methods ==========
    
    def activate(self) -> 'User':
        """Activate user account"""
        if self.status != UserStatus.PENDING:
            raise ValueError(f"Cannot activate from status: {self.status}")
        
        from dataclasses import replace
        return replace(
            self,
            status=UserStatus.ACTIVE,
            updated_at=datetime.now()
        )
    
    def verify_email(self) -> 'User':
        """Mark email as verified"""
        if self.email_verified:
            return self
        
        from dataclasses import replace
        return replace(
            self,
            email_verified=True,
            updated_at=datetime.now()
        )
    
    def record_login(self) -> 'User':
        """Record successful login"""
        from dataclasses import replace
        return replace(
            self,
            last_login_at=datetime.now(),
            failed_login_attempts=0,
            account_locked_until=None,
            updated_at=datetime.now()
        )
    
    def record_failed_login(self) -> 'User':
        """Record failed login attempt"""
        new_attempts = self.failed_login_attempts + 1
        
        # Lock account after 5 failed attempts for 15 minutes
        lock_until = None
        if new_attempts >= 5:
            from datetime import timedelta
            lock_until = datetime.now() + timedelta(minutes=15)
        
        from dataclasses import replace
        return replace(
            self,
            failed_login_attempts=new_attempts,
            account_locked_until=lock_until,
            updated_at=datetime.now()
        )
    
    def change_password(self, new_hash: str) -> 'User':
        """Change password"""
        from dataclasses import replace
        return replace(
            self,
            password_hash=new_hash,
            password_changed_at=datetime.now(),
            updated_at=datetime.now()
        )
```

### **📁 3. Aggregates**

```python
# 📄 domain/aggregates/UserAggregate.py
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from ..entities import User, UserEmail, UserPhone, UserAddress, UserProfile
from ..value_objects import UserId, EmailAddress, PhoneNumber, Address

@dataclass
class UserAggregate:
    """
    Aggregate Root that brings together all user-related entities
    Ensures consistency across all user data
    """
    user: User
    profile: Optional[UserProfile] = None
    emails: List[UserEmail] = field(default_factory=list)
    phones: List[UserPhone] = field(default_factory=list)
    addresses: List[UserAddress] = field(default_factory=list)
    
    # ========== Email Management ==========
    
    def add_email(self, email_address: EmailAddress, 
                  contact_type: str = "PRIMARY",
                  set_as_default: bool = False) -> None:
        """Add new email to user"""
        
        # Check if email already exists
        existing = self.get_email_by_address(email_address.value)
        if existing:
            raise ValueError(f"Email {email_address.value} already exists")
        
        # If this is the first email, it must be default
        if not self.emails:
            set_as_default = True
        
        # Create new UserEmail entity
        new_email = UserEmail(
            user_id=self.user.id.value,
            email=email_address,
            contact_type=contact_type,
            is_default=set_as_default,
            is_verified=False
        )
        
        # If setting as default, unset previous default
        if set_as_default:
            for email in self.emails:
                email.is_default = False
        
        self.emails.append(new_email)
    
    def remove_email(self, email_value: str) -> None:
        """Remove email from user"""
        email_to_remove = self.get_email_by_address(email_value)
        if not email_to_remove:
            raise ValueError(f"Email {email_value} not found")
        
        # Cannot remove default email if it's the only one
        if email_to_remove.is_default and len(self.emails) == 1:
            raise ValueError("Cannot remove the only email address")
        
        # If removing default, set another email as default
        if email_to_remove.is_default:
            other_emails = [e for e in self.emails if e.email.value != email_value]
            if other_emails:
                # Set first primary email as default, or first email
                primary_emails = [e for e in other_emails if e.contact_type == "PRIMARY"]
                if primary_emails:
                    primary_emails[0].is_default = True
                else:
                    other_emails[0].is_default = True
        
        self.emails = [e for e in self.emails if e.email.value != email_value]
    
    def set_default_email(self, email_value: str) -> None:
        """Set a specific email as default"""
        new_default = self.get_email_by_address(email_value)
        if not new_default:
            raise ValueError(f"Email {email_value} not found")
        
        # Unset current default
        for email in self.emails:
            if email.is_default:
                email.is_default = False
        
        # Set new default
        new_default.is_default = True
        new_default.contact_type = "PRIMARY"  # Default must be primary
    
    def get_default_email(self) -> Optional[UserEmail]:
        """Get user's default email"""
        for email in self.emails:
            if email.is_default:
                return email
        return None
    
    def get_email_by_address(self, email_value: str) -> Optional[UserEmail]:
        """Find email by address"""
        for email in self.emails:
            if email.email.value == email_value:
                return email
        return None
    
    # ========== Address Management ==========
    
    def add_address(self, address: Address, 
                    contact_type: str = "HOME",
                    set_as_default: bool = False) -> None:
        """Add new address to user"""
        
        # Create new UserAddress entity
        new_address = UserAddress(
            user_id=self.user.id.value,
            address=address,
            contact_type=contact_type,
            is_default=set_as_default
        )
        
        # If setting as default, unset previous defaults of same type
        if set_as_default:
            for addr in self.addresses:
                if addr.contact_type == contact_type:
                    addr.is_default = False
        
        self.addresses.append(new_address)
    
    def get_address_by_type(self, address_type: str) -> List[UserAddress]:
        """Get addresses of specific type"""
        return [addr for addr in self.addresses if addr.contact_type == address_type]
    
    def get_default_address(self, address_type: str = "HOME") -> Optional[UserAddress]:
        """Get default address of specific type"""
        addresses = self.get_address_by_type(address_type)
        for addr in addresses:
            if addr.is_default:
                return addr
        return addresses[0] if addresses else None
    
    # ========== Phone Management ==========
    
    def add_phone(self, phone: PhoneNumber, 
                  contact_type: str = "MOBILE",
                  set_as_default: bool = False) -> None:
        """Add new phone to user"""
        
        # Create new UserPhone entity
        new_phone = UserPhone(
            user_id=self.user.id.value,
            phone=phone,
            contact_type=contact_type,
            is_default=set_as_default,
            is_verified=False
        )
        
        # If setting as default, unset previous defaults of same type
        if set_as_default:
            for ph in self.phones:
                if ph.contact_type == contact_type:
                    ph.is_default = False
        
        self.phones.append(new_phone)
    
    def get_phone_by_type(self, phone_type: str) -> List[UserPhone]:
        """Get phones of specific type"""
        return [ph for ph in self.phones if ph.contact_type == phone_type]
    
    # ========== Profile Management ==========
    
    def update_profile(self, **kwargs) -> None:
        """Update user profile"""
        if not self.profile:
            raise ValueError("Profile not initialized")
        
        # Create updated profile
        from dataclasses import replace
        updated_profile = replace(
            self.profile,
            **kwargs,
            updated_at=datetime.now()
        )
        self.profile = updated_profile
    
    # ========== Aggregate Validation ==========
    
    def validate_aggregate(self) -> List[str]:
        """Validate aggregate state"""
        errors = []
        
        # Must have at least one email
        if not self.emails:
            errors.append("User must have at least one email")
        
        # Must have exactly one default email
        default_emails = [e for e in self.emails if e.is_default]
        if len(default_emails) != 1:
            errors.append(f"User must have exactly one default email (found {len(default_emails)})")
        
        # Default email must be verified (if there are verified emails)
        if self.emails and any(e.is_verified for e in self.emails):
            default = self.get_default_email()
            if default and not default.is_verified:
                errors.append("Default email must be verified")
        
        # Check for duplicate emails
        email_values = [e.email.value for e in self.emails]
        if len(email_values) != len(set(email_values)):
            errors.append("Duplicate email addresses found")
        
        return errors
```

### **📁 4. Repository Interfaces**

```python
# 📄 domain/repositories/interfaces/UserRepository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from ...entities import User
from ...aggregates import UserAggregate
from ...value_objects import UserId

class UserRepository(ABC):
    """Repository interface for User aggregate"""
    
    @abstractmethod
    def get_by_id(self, user_id: UserId) -> Optional[UserAggregate]:
        """Get complete user aggregate by ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserAggregate]:
        """Get user by email address"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def save(self, aggregate: UserAggregate) -> UserAggregate:
        """Save complete user aggregate"""
        pass
    
    @abstractmethod
    def delete(self, user_id: UserId) -> bool:
        """Delete user"""
        pass

# 📄 domain/repositories/interfaces/EmailRepository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ...entities import UserEmail
from ...value_objects import UserId

class EmailRepository(ABC):
    """Repository for user emails"""
    
    @abstractmethod
    def get_user_emails(self, user_id: UserId) -> List[UserEmail]:
        """Get all emails for a user"""
        pass
    
    @abstractmethod
    def add_email(self, user_email: UserEmail) -> UserEmail:
        """Add new email for user"""
        pass
    
    @abstractmethod
    def remove_email(self, user_id: UserId, email: str) -> bool:
        """Remove email from user"""
        pass
    
    @abstractmethod
    def set_default_email(self, user_id: UserId, email: str) -> bool:
        """Set default email for user"""
        pass

# 📄 domain/repositories/specifications/UserSpecification.py
from abc import ABC, abstractmethod
from typing import List
from ...entities import User

class UserSpecification(ABC):
    """Specification pattern for querying users"""
    
    @abstractmethod
    def is_satisfied_by(self, user: User) -> bool:
        """Check if user satisfies specification"""
        pass

class ActiveUserSpecification(UserSpecification):
    """Specification for active users"""
    
    def is_satisfied_by(self, user: User) -> bool:
        return user.is_active

class VerifiedEmailSpecification(UserSpecification):
    """Specification for users with verified email"""
    
    def is_satisfied_by(self, user: User) -> bool:
        return user.email_verified

class RoleSpecification(UserSpecification):
    """Specification for users with specific role"""
    
    def __init__(self, role):
        self.role = role
    
    def is_satisfied_by(self, user: User) -> bool:
        return user.has_role(self.role)

class CompositeSpecification(UserSpecification):
    """Combine multiple specifications"""
    
    def __init__(self, *specs):
        self.specifications = specs
    
    def is_satisfied_by(self, user: User) -> bool:
        return all(spec.is_satisfied_by(user) for spec in self.specifications)
```

---

## 🗄️ **Database Schema (SQLAlchemy Models)**

```python
# 📄 infrastructure/persistence/models/UserModel.py
from sqlalchemy import Column, String, Enum, Boolean, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class UserModel(Base):
    """SQLAlchemy model for User entity"""
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    status = Column(Enum('pending', 'active', 'suspended', 'banned', 'deleted'), 
                   default='pending')
    roles = Column(JSON, default=['user'])  # Store as JSON array
    
    # Authentication flags
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    password_changed_at = Column(DateTime, default=datetime.utcnow)
    
    # Preferences
    preferences = Column(JSON, default={
        "email_notifications": True,
        "sms_notifications": False,
        "newsletter": True,
        "theme": "light",
        "language": "en"
    })
    
    # Relationships (lazy loading)
    emails = relationship("UserEmailModel", back_populates="user", 
                         cascade="all, delete-orphan")
    phones = relationship("UserPhoneModel", back_populates="user",
                         cascade="all, delete-orphan")
    addresses = relationship("UserAddressModel", back_populates="user",
                            cascade="all, delete-orphan")
    profile = relationship("UserProfileModel", back_populates="user",
                          uselist=False, cascade="all, delete-orphan")

# 📄 infrastructure/persistence/models/UserEmailModel.py
class UserEmailModel(Base):
    """SQLAlchemy model for User-Email relationship"""
    __tablename__ = 'user_emails'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    provider = Column(String(50))
    contact_type = Column(String(20), default='primary')
    is_verified = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    
    # Composite unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'email', name='uq_user_email'),
    )
    
    # Relationships
    user = relationship("UserModel", back_populates="emails")

# 📄 infrastructure/persistence/models/UserAddressModel.py
class UserAddressModel(Base):
    """SQLAlchemy model for User-Address relationship"""
    __tablename__ = 'user_addresses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    
    # Address fields
    street_line1 = Column(String(255), nullable=False)
    street_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(50), default='USA')
    
    # Metadata
    contact_type = Column(String(20), default='home')
    is_default = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("UserModel", back_populates="addresses")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_address_type', 'user_id', 'contact_type'),
    )

# 📄 infrastructure/persistence/models/UserPhoneModel.py
class UserPhoneModel(Base):
    """SQLAlchemy model for User-Phone relationship"""
    __tablename__ = 'user_phones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    
    # Phone fields
    phone_number = Column(String(50), nullable=False, index=True)
    country_code = Column(String(5))
    formatted_number = Column(String(50))
    
    # Metadata
    contact_type = Column(String(20), default='mobile')
    is_verified = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("UserModel", back_populates="phones")
    
    # Composite unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'phone_number', name='uq_user_phone'),
    )

# 📄 infrastructure/persistence/models/UserProfileModel.py
class UserProfileModel(Base):
    """SQLAlchemy model for User Profile"""
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.id'), unique=True, nullable=False, index=True)
    
    # Profile fields
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    display_name = Column(String(100))
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20))
    preferred_language = Column(String(10), default='en')
    timezone = Column(String(50), default='UTC')
    bio = Column(Text)
    avatar_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("UserModel", back_populates="profile")
```

---

## 🚀 **Usage Examples**

```python
# 📄 examples/user_registration.py
from domain.value_objects import UserId, EmailAddress, PhoneNumber, Address
from domain.entities import User, UserProfile, UserEmail, UserPhone, UserAddress
from domain.aggregates import UserAggregate

def example_user_registration():
    """Complete example of user registration"""
    
    # 1. Create user ID
    user_id = UserId.generate()
    
    # 2. Create main user entity
    user = User(
        id=user_id,
        username="john_doe",
        password_hash="hashed_password_123",
        status="active"
    )
    
    # 3. Create user profile
    profile = UserProfile(
        user_id=user_id,
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        preferred_language="en"
    )
    
    # 4. Add emails
    email1 = EmailAddress("john.doe@gmail.com")
    email2 = EmailAddress("john.doe@company.com")
    
    # 5. Add phones
    phone1 = PhoneNumber("+1-555-123-4567")
    phone2 = PhoneNumber("+1-555-987-6543")
    
    # 6. Add addresses
    address1 = Address(
        street_line1="123 Main St",
        city="New York",
        state="NY",
        postal_code="10001",
        country="USA"
    )
    
    address2 = Address(
        street_line1="456 Office Blvd",
        street_line2="Suite 100",
        city="New York",
        state="NY",
        postal_code="10002",
        country="USA"
    )
    
    # 7. Create aggregate
    user_aggregate = UserAggregate(
        user=user,
        profile=profile,
        emails=[
            UserEmail(user_id=user_id.value, email=email1, is_default=True),
            UserEmail(user_id=user_id.value, email=email2, contact_type="work")
        ],
        phones=[
            UserPhone(user_id=user_id.value, phone=phone1, is_default=True),
            UserPhone(user_id=user_id.value, phone=phone2, contact_type="work")
        ],
        addresses=[
            UserAddress(user_id=user_id.value, address=address1, is_default=True),
            UserAddress(user_id=user_id.value, address=address2, contact_type="work")
        ]
    )
    
    # 8. Validate aggregate
    errors = user_aggregate.validate_aggregate()
    if errors:
        print("Validation errors:", errors)
    else:
        print("✅ User aggregate is valid")
    
    # 9. Business operations
    print(f"Default email: {user_aggregate.get_default_email().email.value}")
    print(f"Active: {user_aggregate.user.is_active}")
    print(f"Has work address: {len(user_aggregate.get_address_by_type('work')) > 0}")
    
    return user_aggregate

if __name__ == "__main__":
    user_aggregate = example_user_registration()
```

---

## ✅ **Benefits of This Design**

### **1. Separation of Concerns**
- Each class has single responsibility
- Changes to email don't affect user entity

### **2. Loose Coupling**
- Entities reference each other through IDs
- Easy to swap implementations

### **3. Scalability**
- Can scale emails, addresses independently
- Database joins are explicit and optimized

### **4. Testability**
- Pure domain models are easy to test
- No database dependencies in unit tests

### **5. Business Logic Encapsulation**
- Validation rules in value objects
- Business rules in entities/aggregates

### **6. Database Agnostic**
- Domain models don't know about persistence
- Easy to switch databases

---

## 📈 **Performance Considerations**

### **1. Database Indexing Strategy**
```sql
-- Essential indexes
CREATE INDEX idx_user_emails_user_id ON user_emails(user_id);
CREATE INDEX idx_user_emails_default ON user_emails(user_id, is_default);
CREATE INDEX idx_user_phones_user_id ON user_phones(user_id);
CREATE INDEX idx_user_addresses_user_type ON user_addresses(user_id, contact_type);
```

### **2. Caching Strategy**
- Cache complete UserAggregate by user_id
- Cache frequently accessed emails/phones
- Invalidate cache on updates

### **3. Query Optimization**
- Use eager loading for frequently accessed relationships
- Implement read models for common queries
- Consider materialized views for complex aggregations

---

## 🚀 **Next Steps & Best Practices**

### **Phase 4: Implement Repository Pattern**
1. Create SQLAlchemy implementations of repositories
2. Add unit of work pattern for transactions
3. Implement caching layer

### **Phase 5: Application Services**
1. Create use case handlers
2. Implement command/query separation
3. Add validation services

### **Phase 6: API Layer**
1. Create REST/GraphQL endpoints
2. Add authentication/authorization
3. Implement rate limiting

### **Phase 7: Monitoring & Observability**
1. Add logging
2. Implement metrics collection
3. Set up distributed tracing

---

## 🔧 **Development Workflow**

1. **Start with domain models** (what you have now)
2. **Add repository interfaces** for persistence abstraction
3. **Implement application services** with use cases
4. **Create infrastructure layer** (database, external services)
5. **Add API/UI layer** on top
6. **Implement testing** at each layer

This design follows **Clean Architecture** and **Domain-Driven Design** principles, making your system maintainable, scalable, and testable for years to come. 🎯