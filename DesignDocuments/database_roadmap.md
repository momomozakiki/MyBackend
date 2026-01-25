Here's a **revised roadmap specifically for creating universal/reusable database models** for Users, Products, and Addresses. This follows your initial vision of independent, modular models that can be extended per-project.

---

## 🗺️ **Universal Models Roadmap: 5 Phases**

### **🎯 Phase 0: Universal Design Foundation (1-2 days)**
**Goal:** Define core principles for universal models

```
universal_models/
├── DESIGN_PRINCIPLES/
│   ├── core_philosophy.md    # "Independent models, relationships added per-project"
│   ├── compatibility_goals.md  # "Support SQLAlchemy 1.4+, Python 3.8+"
│   └── extension_strategy.md  # "How projects extend base models"
├── REQUIREMENTS/
│   ├── user_requirements.md  # Basic user fields without relationships
│   ├── product_requirements.md  # Product fields without category dependencies
│   └── address_requirements.md  # Address fields without user constraints
└── ARCHITECTURE/
    └── adr-001-universal-models.md
```

**Key Deliverables:**
- ✅ **Universal Model Principles** document
- ✅ **Field definitions** for each model (minimal viable fields)
- ✅ **Extension patterns** documented (how projects add relationships)
- ✅ **Versioning strategy** (semantic versioning for breaking changes)

**Example `core_philosophy.md`:**
```markdown
# Universal Models Core Philosophy

## Independence First
- Models must work independently without relationships
- No foreign keys in base models
- No project-specific business logic

## Extension by Composition
- Projects extend base models through inheritance
- Relationships added in project-specific code
- Base models remain unchanged

## Backward Compatibility
- Minor versions: Add fields, never remove
- Major versions: Only for breaking changes
- Always maintain migration paths

## Database Agnostic
- No database-specific features in base models
- Support PostgreSQL, MySQL, SQLite, etc.
- No stored procedures or database triggers
```

---

### **🏗️ Phase 1: Core Model Implementation (Week 1)**
**Goal:** Create independent, relationship-free base models

```
universal_models/
├── universal_models/
│   ├── __init__.py          # Package exports and version
│   ├── base.py             # Base class definition
│   ├── user/
│   │   ├── __init__.py     # User model exports
│   │   ├── model.py        # Base User model
│   │   └── schemas.py      # User schemas (Pydantic)
│   ├── product/
│   │   ├── __init__.py
│   │   ├── model.py        # Base Product model
│   │   └── schemas.py
│   └── address/
│       ├── __init__.py
│       ├── model.py        # Base Address model
│       └── schemas.py
├── pyproject.toml          # Package configuration
├── README.md               # Usage documentation
└── tests/
    ├── unit/
    │   ├── test_user_model.py
    │   ├── test_product_model.py
    │  
Here's a **revised roadmap specifically for creating universal/reusable database models** for Users, Products, and Addresses. This follows your initial vision of independent, modular models that can be extended per-project.

---

## 🗺️ **Universal Models Roadmap: 5 Phases**

### **🎯 Phase 0: Universal Design Foundation (1-2 days)**
**Goal:** Define core principles for universal models

```
```
universal_models/
├── DESIGN_PRINCIPLES/
│   ├── core_philosophy.md    # "Independent models, relationships added per-project"
│   ├── compatibility_goals.md  # "Support SQLAlchemy 1.4+, Python 3.8+"
│   └── extension_strategy.md  # "How projects extend base models"
├── REQUIREMENTS/
│   ├── user_requirements.md  # Basic user fields without relationships
│   ├── product_requirements.md  # Product fields without category dependencies
│   └── address_requirements.md  # Address fields without user constraints
└── ARCHITECTURE/
    └── adr-001-universal-models.md
```
```

**Key Deliverables:**
- ✅ **Universal Model Principles** document
- ✅ **Field definitions** for each model (minimal viable fields)
- ✅ **Extension patterns** documented (how projects add relationships)
- ✅ **Versioning strategy** (semantic versioning for breaking changes)

**Example `core_philosophy.md`:**
```markdown
# Universal Models Core Philosophy

## Independence First
- Models must work independently without relationships
- No foreign keys in base models
- No project-specific business logic

## Extension by Composition
- Projects extend base models through inheritance
- Relationships added in project-specific code
- Base models remain unchanged

## Backward Compatibility
- Minor versions: Add fields, never remove
- Major versions: Only for breaking changes
- Always maintain migration paths

## Database Agnostic
- No database-specific features in base models
- Support PostgreSQL, MySQL, SQLite, etc.
- No stored procedures or database triggers
```

---

### **🏗️ Phase 1: Core Model Implementation (Week 1)**
**Goal:** Create independent, relationship-free base models

```
universal_models/
├── universal_models/
│   ├── __init__.py          # Package exports and version
│   ├── base.py             # Base class definition
│   ├── user/
│   │   ├── __init__.py     # User model exports
│   │   ├── model.py        # Base User model
│   │   └── schemas.py      # User schemas (Pydantic)
│   ├── product/
│   │   ├── __init__.py
│   │   ├── model.py        # Base Product model
│   │   └── schemas.py
│   └── address/
│       ├── __init__.py
│       ├── model.py        # Base Address model
│       └── schemas.py
├── pyproject.toml          # Package configuration
├── README.md               # Usage documentation
└── tests/
    ├── unit/
    │   ├── test_user_model.py
    │   ├── test_product_model.py
    │   └── test_address_model.py
    └── conftest.py
```

**Example File: `universal_models/user/model.py`**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from ..base import Base
from typing import Optional

class User(Base):
    """
    Universal User model - no relationships, no project-specific fields
    
    This model is designed to be:
    ✅ Independent - works without any other models
    ✅ Extendable - projects can inherit and add relationships
    ✅ Stable - fields won't change between minor versions
    ✅ Minimal - only essential fields for most projects
    
    Projects that need relationships should extend this class:
    
    from universal_models.user import User as BaseUser
    
    class User(BaseUser):
        __tablename__ = "users"
        __mapper_args__ = {"polymorphic_identity": "project_user"}
        
        # Add project-specific relationships here
        addresses = relationship("Address")
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    provider = Column(String(50), default="email", nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, name={self.name})"
```

**Example File: `universal_models/base.py`**
```python
from sqlalchemy.orm import declarative_base, DeclarativeBase
from typing import Type

# Support both SQLAlchemy 1.4 and 2.0 styles
try:
    # SQLAlchemy 2.0+ style
    class Base(DeclarativeBase):
        """Modern SQLAlchemy 2.0 base class"""
        pass
except ImportError:
    # Fallback to SQLAlchemy 1.4 style
    Base = declarative_base()

# Type alias for better type hinting
BaseType = Type[Base]

__all__ = ["Base", "BaseType"]
```

**Key Deliverables:**
- ✅ **Three independent models**: User, Product, Address
- ✅ **No relationships** in base models
- ✅ **Type hints** for modern Python compatibility
- ✅ **Comprehensive docstrings** explaining extension patterns
- ✅ **Unit tests** for each model's core functionality

---

### **📋 Phase 2: Schema Definitions & Validation (Week 2)**
**Goal:** Create Pydantic schemas for data validation

```
universal_models/
├── universal_models/
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base.py         # Base schema classes
│   │   ├── user_schemas.py # User schemas
│   │   ├── product_schemas.py
│   │   └── address_schemas.py
│   └── validators/
│       ├── __init__.py
│       ├── email_validator.py
│       └── phone_validator.py
└── tests/
    └── unit/
        └── test_schemas.py
```

**Example File: `universal_models/schemas/user_schemas.py`**
```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from ..validators.email_validator import validate_email_format

class UserBase(BaseModel):
    """
    Base schema for user operations - shared fields
    """
    name: Optional[str] = Field(
        None,
        max_length=255,
        description="User's full name",
        example="John Doe"
    )

class UserCreate(UserBase):
    """
    Schema for creating a new user
    
    This schema validates input data before it reaches the database.
    Projects can extend this schema with additional fields as needed.
    
    Example extension in a project:
    
    from universal_models.schemas.user_schemas import UserCreate as BaseUserCreate
    
    class UserCreate(BaseUserCreate):
        phone_number: Optional[str] = None
        agree_to_terms: bool = Field(..., description="User must agree to terms")
    """
    email: EmailStr = Field(
        ...,
        description="User's email address - must be unique across the system",
        example="user@example.com"
    )
    
    @validator('email')
    def validate_email(cls, v):
        return validate_email_format(v)
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe"
            }
        }

class UserResponse(UserBase):
    """
    Schema for user responses - what clients receive
    
    This schema controls what data is exposed to API clients.
    Sensitive fields like passwords are never included here.
    """
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True  # Allow SQLAlchemy model conversion
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "name": "John Doe",
                "is_active": true,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
```

**Key Deliverables:**
- ✅ **Input schemas** for creating/updating data
- ✅ **Output schemas** for API responses
- ✅ **Validation logic** for universal rules (email format, etc.)
- ✅ **Extension-friendly design** (projects can inherit schemas)
- ✅ **Example data** for API documentation

---

### **📦 Phase 3: Package Structure & Distribution (Week 3)**
**Goal:** Make the package installable and reusable

```
universal_models/
├── universal_models/
│   ├── __init__.py        # Package metadata and exports
│   ├── __version__.py     # Version management
│   └── utils/
│       ├── __init__.py
│       └── model_helpers.py  # Helper functions for model extension
├── pyproject.toml         # Modern build system configuration
├── README.md              # Installation and usage guide
├── CHANGELOG.md           # Version history
├── LICENSE                # MIT/Apache 2.0 license
├── .gitignore
└── examples/
    ├── auth_service/      # Example: Authentication service using only User
    │   ├── main.py
    │   └── requirements.txt
    ├── ecom_service/      # Example: E-commerce service with relationships
    │   ├── models.py      # Extended models with relationships
    │   └── requirements.txt
    └── logistics_service/ # Example: Logistics service using Address independently
        ├── main.py
        └── requirements.txt
```

**Example File: `universal_models/__init__.py`**
```python
"""
Universal SQLAlchemy Models Package

A collection of independent, reusable database models that can be
extended per-project. Import only what you need, add relationships
when required.

Core Philosophy:
✅ Independence - models work without relationships
✅ Extendability - projects inherit and customize
✅ Stability - backward compatibility guaranteed
✅ Minimalism - only essential fields included

Basic Usage:
    from universal_models.user import User
    from universal_models.base import Base

Extended Usage (adding relationships):
    from universal_models.user import User as BaseUser
    from universal_models.address import Address as BaseAddress
    
    class User(BaseUser):
        addresses = relationship("Address")

Version: 0.1.0
"""

from .base import Base
from .__version__ import __version__, __author__, __email__

# Export core models for easy import
from .user import User
from .product import Product
from .address import Address

# Export schemas
from .schemas.user_schemas import UserCreate, UserResponse
from .schemas.product_schemas import ProductCreate, ProductResponse
from .schemas.address_schemas import AddressCreate, AddressResponse

__all__ = [
    "Base",
    "User",
    "Product", 
    "Address",
    "UserCreate",
    "UserResponse",
    "ProductCreate",
    "ProductResponse",
    "AddressCreate",
    "AddressResponse",
    "__version__",
    "__author__",
    "__email__"
]

# Package metadata
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "Universal SQLAlchemy models for multiple projects"
```

**Example File: `pyproject.toml`**
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "universal_models"
version = "0.1.0"
description = "Universal SQLAlchemy models for multiple projects"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
maintainers = [
    {name = "Your Name", email = "your.email@example.com"},
]
dependencies = [
    "sqlalchemy>=1.4.0,<3.0.0",  # Support both 1.4 and 2.0
    "pydantic>=1.10.0,<3.0.0",   # Support Pydantic v1 and v2
]
optional-dependencies = {
    test = [
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "sqlalchemy-utils>=0.41.0",
    ],
    dev = [
        "black>=23.0.0",
        "isort>=5.12.0",
        "mypy>=1.0.0",
        "pre-commit>=3.0.0",
    ],
}
requires-python = ">=3.8"

[project.urls]
Homepage = "https://github.com/yourusername/universal_models"
Repository = "https://github.com/yourusername/universal_models"
Documentation = "https://github.com/yourusername/universal_models/blob/main/README.md"
Changelog = "https://github.com/yourusername/universal_models/blob/main/CHANGELOG.md"

[tool.setuptools]
packages = ["universal_models"]
package-dir = {"" = "."}

[tool.setuptools.package-data]
universal_models = ["py.typed"]

[tool.black]
line-length = 119
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.isort]
profile = "black"
line_length = 119
```

**Key Deliverables:**
- ✅ **Installable Python package** (`pip install universal_models`)
- ✅ **Version management** with semantic versioning
- ✅ **Comprehensive documentation** (README, examples)
- ✅ **License file** (MIT/Apache 2.0 recommended)
- ✅ **Example projects** showing different usage patterns
- ✅ **Type hinting support** (`py.typed` file)

---

### **🔄 Phase 4: Extension Patterns & Documentation (Week 4)**
**Goal:** Document how projects can extend and customize models

```
universal_models/
├── docs/
│   ├── EXTENSION_GUIDE.md    # How to extend models
│   ├── RELATIONSHIP_PATTERNS.md  # Common relationship patterns
│   ├── MIGRATION_GUIDE.md    # Upgrading between versions
│   └── BEST_PRACTICES.md     # Usage recommendations
├── templates/
│   ├── model_extension.py.j2  # Jinja template for model extensions
│   └── api_example.py.j2     # API example template
└── examples/
    ├── advanced/
    │   ├── multi_tenant.py   # Multi-tenant extension example
    │   └── soft_delete.py    # Soft delete pattern
    └── performance/
        ├── indexing_strategy.py  # Indexing recommendations
        └── caching_patterns.py   # Caching strategies
```

**Example File: `docs/EXTENSION_GUIDE.md`**
```markdown
# Universal Models Extension Guide

## 🎯 Core Extension Principles

### 1. Never Modify Base Models
```python
# ❌ NEVER do this - breaks package integrity
from universal_models.user import User
User.new_field = Column(String(100))  # This corrupts the base model

# ✅ ALWAYS extend through inheritance
from universal_models.user import User as BaseUser

class User(BaseUser):
    __tablename__ = "users"
    __mapper_args__ = {"polymorphic_identity": "project_user"}
    
    new_field = Column(String(100))
```

### 2. Add Relationships in Project Code
```python
# ecom_project/models.py
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from universal_models.user import User as BaseUser
from universal_models.address import Address as BaseAddress

class User(BaseUser):
    """Extended User with address relationships"""
    __tablename__ = "users"
    __mapper_args__ = {"polymorphic_identity": "ecom_user"}
    
    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

class Address(BaseAddress):
    """Extended Address with user relationship"""
    __tablename__ = "addresses"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="addresses")
```

### 3. Schema Extension Patterns
```python
# ecom_project/schemas.py
from universal_models.schemas.user_schemas import UserCreate as BaseUserCreate
from pydantic import Field

class UserCreate(BaseUserCreate):
    """Extended user creation schema with e-commerce fields"""
    phone_number: str = Field(..., description="User's phone number for order updates")
    marketing_consent: bool = Field(False, description="Agree to marketing emails")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "customer@example.com",
                "name": "Jane Smith",
                "phone_number": "+1234567890",
                "marketing_consent": true
            }
        }
```

## 🚀 Advanced Extension Patterns

### Pattern 1: Multi-Tenant Extension
```python
from universal_models.user import User as BaseUser

class TenantUser(BaseUser):
    """User model with tenant isolation"""
    __tablename__ = "users"
    __mapper_args__ = {"polymorphic_identity": "tenant_user"}
    
    tenant_id = Column(String(36), index=True, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('email', 'tenant_id', name='uq_user_email_tenant'),
    )
```

### Pattern 2: Soft Delete Extension
```python
from universal_models.user import User as BaseUser
from sqlalchemy import Boolean, DateTime

class SoftDeleteUser(BaseUser):
    """User model with soft delete capability"""
    __tablename__ = "users"
    __mapper_args__ = {"polymorphic_identity": "soft_delete_user"}
    
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    @classmethod
    def get_active_users(cls, session):
        return session.query(cls).filter(cls.is_deleted == False)
```

## 🛠️ Migration Strategies

### Adding Foreign Keys to Existing Tables
```python
# alembic/versions/add_user_address_fk.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Step 1: Add nullable column first
    op.add_column('addresses', sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Step 2: Add index for performance
    op.create_index('ix_addresses_user_id', 'addresses', ['user_id'])
    
    # Step 3: Add foreign key constraint (optional, can be done in application logic)
    # op.create_foreign_key(
    #    'fk_addresses_user_id', 'addresses', 'users',
    #    ['user_id'], ['id'], ondelete='SET NULL'
    # )

def downgrade():
    # op.drop_constraint('fk_addresses_user_id', 'addresses', type_='foreignkey')
    op.drop_index('ix_addresses_user_id', 'addresses')
    op.drop_column('addresses', 'user_id')
```

## 📋 Best Practices Checklist

✅ **Import selectively** - only import models you need  
✅ **Extend, don't modify** - always inherit from base models  
✅ **Make foreign keys nullable** - allows gradual adoption  
✅ **Add indexes** - always index foreign key columns  
✅ **Version your extensions** - document breaking changes  
✅ **Test migrations** - test on staging data before production  
✅ **Document customizations** - maintain project-specific docs  

## 🔗 Related Resources

- [SQLAlchemy Inheritance Documentation](https://docs.sqlalchemy.org/en/20/orm/inheritance.html)
- [Pydantic Schema Extension Guide](https://docs.pydantic.dev/latest/usage/schema/)
- [Alembic Migration Best Practices](https://alembic.sqlalchemy.org/en/latest/bestpractices.html)
```

**Key Deliverables:**
- ✅ **Comprehensive extension guide** with code examples
- ✅ **Common patterns documentation** (multi-tenant, soft delete, etc.)
- ✅ **Migration strategies** for adding relationships to existing databases
- ✅ **Best practices checklist** for developers
- ✅ **Advanced examples** showing real-world usage patterns

---

### **🚀 Phase 5: Publishing & Maintenance (Week 5+)**
**Goal:** Publish to PyPI and establish maintenance processes
```

```
universal_models/
├── .github/
│   ├── workflows/
│   │   ├── test.yml          # CI pipeline
│   │   ├── publish.yml       # PyPI publishing
│   │   └── docs.yml          # Documentation build
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── scripts/
│   ├── build_package.sh      # Build distribution
│   ├── publish_test_pypi.sh  # Publish to test PyPI
│   └── update_version.sh     # Version bump script
├── CONTRIBUTING.md           # Contribution guidelines
├── SECURITY.md              # Security policy
├── SUPPORT.md               # Support channels
└── ROADMAP.md               # Future development plans
```

```
**Key Deliverables:**
- ✅ **GitHub Actions workflows** for automated testing and publishing
- ✅ **PyPI publishing pipeline** (test PyPI first, then production)
- ✅ **Version control strategy** (semantic versioning)
- ✅ **Maintenance processes** (issue templates, contribution guidelines)
- ✅ **Security policy** for vulnerability reporting
- ✅ **Long-term roadmap** for future model additions

---

## 🎯 **Universal Models File Structure Summary**

### **Final Package Structure**
```
```
universal_models/
├── universal_models/           # Core package
│   ├── __init__.py            # Package exports and metadata
│   ├── __version__.py         # Version management
│   ├── base.py               # Base class definition
│   ├── utils/                # Helper utilities
│   ├── user/                 # User model module
│   │   ├── __init__.py
│   │   ├── model.py          # Base User model
│   │   └── schemas.py        # User schemas
│   ├── product/              # Product model module
│   │   ├── __init__.py
│   │   ├── model.py
│   │   └── schemas.py
│   ├── address/              # Address model module
│   │   ├── __init__.py
│   │   ├── model.py
│   │   └── schemas.py
│   └── validators/           # Validation utilities
│       ├── __init__.py
│       ├── email_validator.py
│       └── phone_validator.py
├── docs/                     # Documentation
│   ├── EXTENSION_GUIDE.md
│   ├── RELATIONSHIP_PATTERNS.md
│   ├── MIGRATION_GUIDE.md
│   └── BEST_PRACTICES.md
├── examples/                 # Usage examples
│   ├── auth_service/        # Auth service example (User only)
│   ├── ecom_service/        # E-commerce example (User + Address relationships)
│   └── logistics_service/   # Logistics example (Address only)
├── tests/                    # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── conftest.py
├── .github/                  # GitHub workflows
│   └── workflows/
├── scripts/                  # Utility scripts
├── pyproject.toml            # Package configuration
├── README.md                 # Main documentation
├── CHANGELOG.md              # Version history
├── LICENSE                   # License file
├── CONTRIBUTING.md           # Contribution guidelines
└── ROADMAP.md                # Future development plans
```
```

---

## 🚀 **Key Principles for Universal Models Success**

### **1. Independence Over Integration**
```python
# ✅ CORRECT: Independent models
class User(Base):
    email = Column(String(255), unique=True)

class Address(Base):
    street = Column(String(255))
    # No user_id foreign key in base model

# ❌ INCORRECT: Tightly coupled models
class Address(Base):
    user_id = Column(Integer, ForeignKey("users.id"))  # Forces relationship
```

### **2. Extension by Inheritance**
```python
# ✅ CORRECT: Extension pattern
from universal_models.user import User as BaseUser

class ProjectUser(BaseUser):
    __tablename__ = "users"
    __mapper_args__ = {"polymorphic_identity": "project_user"}
    
    # Add project-specific fields and relationships here
    team_id = Column(Integer, nullable=True)

# ❌ INCORRECT: Modifying base models
from universal_models.user import User
User.team_id = Column(Integer)  # Never modify the base package
```

### **3. Gradual Adoption Strategy**
```python
# ✅ CORRECT: Start simple, add complexity as needed
# Phase 1: Use base models independently
from universal_models.user import User
from universal_models.address import Address

# Phase 2: Add relationships when needed
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from universal_models.user import User as BaseUser
from universal_models.address import Address as BaseAddress

class User(BaseUser):
    addresses = relationship("Address")

class Address(BaseAddress):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
```

### **4. Versioning Responsibility**
```python
# MAJOR version (v1.0.0 -> v2.0.0): Breaking changes
# - Removing fields from base models
# - Changing field types in incompatible ways
# - Removing support for older SQLAlchemy versions

# MINOR version (v1.0.0 -> v1.1.0): Backward compatible additions
# - Adding new optional fields to base models
# - Adding new models (e.g., universal_models.order)
# - Adding support for newer SQLAlchemy versions

# PATCH version (v1.0.0 -> v1.0.1): Bug fixes only
# - Fixing validation logic
# - Documentation improvements
# - Performance optimizations
```

---

## 🎯 **When to Add New Models**

| **Model Type** | **Criteria for Addition** | **Example** |
|----------------|---------------------------|-------------|
| **Core Models** | Needed by >80% of projects | User, Address, Product |
| **Domain Models** | Specific to common domains | Order (e-commerce), Patient (healthcare) |
| **Extension Models** | Built on core models | UserAddress (relationship table) |
| **Utility Models** | Cross-cutting concerns | AuditLog, FileAttachment |

**Decision Process:**
1. **Community demand** - multiple projects requesting the same model
2. **Stability** - the domain is well-understood and stable
3. **Independence** - can be implemented without relationships
4. **Backward compatibility** - won't break existing projects

---

## 💡 **Pro Tips for Universal Model Development**

1. **Start minimal** - add fields only when absolutely necessary
2. **Document everything** - explain why decisions were made
3. **Test extensively** - unit tests for every model and schema
4. **Version carefully** - follow semantic versioning strictly
5. **Listen to users** - gather feedback from real projects
6. **Stay database-agnostic** - avoid database-specific features
7. **Support multiple SQLAlchemy versions** - test against 1.4 and 2.0+
8. **Provide extension templates** - make it easy for projects to extend
9. **Maintain changelog** - document every change clearly
10. **Plan for deprecation** - never remove features abruptly

---

## 🚀 **Getting Started Checklist**

**Week 1: Core Models**
- [ ] Create base.py with SQLAlchemy compatibility
- [ ] Implement User model with essential fields only
- [ ] Implement Address model with no user relationships
- [ ] Implement Product model with minimal fields
- [ ] Write unit tests for each model

**Week 2: Schemas & Validation**
- [ ] Create Pydantic schemas for all models
- [ ] Implement validation logic (email, phone, etc.)
- [ ] Add example data for documentation
- [ ] Test schema validation thoroughly

**Week 3: Package Setup**
- [ ] Configure pyproject.toml for modern builds
- [ ] Create comprehensive README.md
- [ ] Set up GitHub repository with proper structure
- [ ] Add examples for different usage patterns

**Week 4: Documentation**
- [ ] Write EXTENSION_GUIDE.md with real examples
- [ ] Document relationship patterns
- [ ] Create migration guide for existing databases
- [ ] Add best practices checklist

**Week 5: Publication**
- [ ] Set up GitHub Actions for CI/CD
- [ ] Publish to test PyPI
- [ ] Test installation in multiple environments
- [ ] Publish to production PyPI

**This roadmap gives you a clear path to creating truly universal, reusable database models that can serve as the foundation for countless projects while maintaining flexibility and backward compatibility. Start small, think big, and always prioritize independence over integration!** 🎉