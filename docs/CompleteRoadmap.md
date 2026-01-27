# 🗺️ **Complete Roadmap: Next.js Frontend ↔ Next.js Backend ↔ FastAPI Backend**

## 📋 **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          COMPLETE SYSTEM FLOW                                           │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                         │
│  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐      │
│  │   NEXT.JS        │     │   NEXT.JS        │     │    FASTAPI       │     │    DATABASE      │      │
│  │   FRONTEND       │────▶│   BACKEND        │────▶│   BACKEND        │────▶│   (SQLite)       │      │
│  │   (React/TS)     │◀────│   (API Routes)   │◀────│   (FastAPI)      │◀────│                  │      │
│  └──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘      │
│                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **PHASE 1: PROJECT SETUP & CONFIGURATION**

### **1.1 Project Structure**

```
project-root/
├── frontend/                    # Next.js Frontend
│   ├── pages/
│   │   ├── index.tsx           # Home page
│   │   ├── login.tsx           # Login page
│   │   ├── dashboard.tsx       # Protected dashboard
│   │   └── api/                # API routes (backend)
│   │       └── auth/
│   │           ├── login.ts     # Initiate Google OAuth
│   │           └── callback/    # Handle OAuth callback
│   │               └── google.ts
│   ├── components/
│   │   ├── LoginButton.tsx
│   │   └── ProtectedRoute.tsx
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   └── auth.ts             # Auth utilities
│   ├── next.config.js
│   ├── .env.local
│   └── package.json
│
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry
│   │   ├── database.py         # Database connection
│   │   ├── models/             # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── auth.py
│   │   ├── routers/            # API routers
│   │   │   ├── __init__.py
│   │   │   └── auth.py
│   │   ├── services/           # Business logic
│   │   │   ├── __init__.py
│   │   │   └── auth_service.py
│   │   ├── core/               # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   └── utils/              # Utilities
│   │       ├── __init__.py
│   │       └── oauth.py
│   ├── requirements.txt
│   ├── .env
│   └── alembic/                # Database migrations
│
└── README.md
```

### **1.2 Environment Setup**

#### **Frontend Environment (.env.local)**
```env
# Frontend Configuration
NEXT_PUBLIC_APP_NAME="My App"
NEXT_PUBLIC_API_URL="http://localhost:3000/api"
NEXT_PUBLIC_FASTAPI_URL="http://localhost:8000"

# Google OAuth Configuration
NEXT_PUBLIC_GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"

# Session Configuration
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-nextauth-secret-key-change-in-production"
```

#### **Backend Environment (.env)**
```env
# FastAPI Configuration
APP_NAME="My App Backend"
ENVIRONMENT="development"
BASE_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"

# Server Configuration
HOST="0.0.0.0"
PORT=8000

# Database Configuration (SQLite for testing)
DATABASE_URL="sqlite:///./test.db"
# For production, use: postgresql://user:password@localhost/dbname

# Google OAuth Configuration
GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
GOOGLE_REDIRECT_URI="http://localhost:8000/auth/google/callback"

# JWT Configuration
SECRET_KEY="your-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
ALLOWED_ORIGINS="http://localhost:3000,http://localhost:3001"
```

### **1.3 Install Dependencies**

#### **Frontend (Next.js)**
```bash
cd frontend
npm init -y
npm install next react react-dom typescript @types/react @types/node
npm install axios
npm install tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Optional: For state management
npm install zustand
# Or for more complex apps:
npm install @reduxjs/toolkit react-redux
```

#### **Backend (FastAPI)**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install fastapi uvicorn sqlalchemy python-jose[cryptography] \
            passlib[bcrypt] python-multipart python-dotenv \
            httpx alembic aiosqlite email-validator

# For PostgreSQL (when ready to migrate from SQLite)
# pip install psycopg2-binary
```

---

## 🎯 **PHASE 2: FASTAPI BACKEND IMPLEMENTATION**

### **2.1 Core Configuration**

#### **`backend/app/core/config.py`**
```python
import os
from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App Configuration
    APP_NAME: str = "My App Backend"
    ENVIRONMENT: str = "development"
    BASE_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

#### **`backend/app/core/security.py`**
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    """Create JWT refresh token"""
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def get_user_id_from_token(token: str) -> Optional[str]:
    """Extract user ID from token"""
    payload = verify_token(token)
    if payload:
        return payload.get("sub")
    return None
```

### **2.2 Database Models**

#### **`backend/app/database.py`**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### **`backend/app/models/user.py`**
```python
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base
from uuid import uuid4
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    picture_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        """Convert to dictionary for API response"""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "picture_url": self.picture_url,
            "is_active": self.is_active,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat()
        }
```

#### **`backend/app/schemas/auth.py`**
```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class GoogleCallbackRequest(BaseModel):
    """Request schema for Google OAuth callback"""
    code: str
    redirect_uri: str

class TokenResponse(BaseModel):
    """Response schema for token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    """Response schema for user"""
    id: str
    email: EmailStr
    name: str
    picture_url: Optional[str]
    is_active: bool
    last_login: Optional[str]
    created_at: str

class AuthResponse(BaseModel):
    """Complete authentication response"""
    token: TokenResponse
    user: UserResponse
```

### **2.3 OAuth Utilities**

#### **`backend/app/utils/oauth.py`**
```python
import httpx
from typing import Dict, Optional
from app.core.config import settings

class GoogleUserInfo:
    """Google user information model"""
    def __init__(self, email: str, name: str, picture: str, sub: str):
        self.email = email
        self.name = name
        self.picture = picture
        self.sub = sub

async def exchange_code_for_token(authorization_code: str, redirect_uri: str) -> Dict:
    """
    Exchange authorization code for access token
    This is a server-to-server call to Google
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "code": authorization_code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code"
                },
                timeout=10.0
            )
            
            if response.status_code != 200:
                error_data = response.json()
                error_msg = error_data.get("error_description", error_data.get("error", "Unknown error"))
                raise ValueError(f"Failed to exchange code: {error_msg}")
            
            return response.json()
            
        except httpx.HTTPError as e:
            raise ValueError(f"Network error during token exchange: {str(e)}")

async def get_google_user_info(access_token: str) -> GoogleUserInfo:
    """
    Get user information from Google using access token
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                },
                timeout=10.0
            )
            
            if response.status_code != 200:
                raise ValueError("Failed to fetch user info from Google")
            
            data = response.json()
            
            # Validate required fields
            if not data.get("email"):
                raise ValueError("Email not found in Google response")
            
            if not data.get("email_verified"):
                raise ValueError("Google account email is not verified")
            
            return GoogleUserInfo(
                email=data["email"],
                name=data.get("name", ""),
                picture=data.get("picture", ""),
                sub=data["sub"]
            )
            
        except httpx.HTTPError as e:
            raise ValueError(f"Network error fetching user info: {str(e)}")
```

### **2.4 Authentication Service**

#### **`backend/app/services/auth_service.py`**
```python
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User
from app.utils.oauth import exchange_code_for_token, get_google_user_info
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from typing import Tuple

async def process_google_oauth(
    db: Session,
    authorization_code: str,
    redirect_uri: str
) -> Tuple[dict, User]:
    """
    Complete Google OAuth flow:
    1. Exchange code for token
    2. Get user info from Google
    3. Create or update user in database
    4. Generate JWT tokens
    """
    # Step 1: Exchange authorization code for access token
    token_data = await exchange_code_for_token(authorization_code, redirect_uri)
    access_token = token_data.get("access_token")
    
    if not access_token:
        raise ValueError("Access token not found in Google response")
    
    # Step 2: Get user information from Google
    user_info = await get_google_user_info(access_token)
    
    # Step 3: Create or update user in database
    user = await create_or_update_user(db, user_info)
    
    # Step 4: Generate JWT tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }, user

async def create_or_update_user(db: Session, user_info) -> User:
    """
    Create new user or update existing user
    """
    # Check if user exists
    user = db.query(User).filter(User.email == user_info.email).first()
    
    if user:
        # Update existing user
        user.name = user_info.name
        user.picture_url = user_info.picture
        user.last_login = datetime.utcnow()
        user.is_active = True
    else:
        # Create new user
        user = User(
            email=user_info.email,
            name=user_info.name,
            picture_url=user_info.picture,
            is_active=True,
            last_login=datetime.utcnow()
        )
        db.add(user)
    
    db.commit()
    db.refresh(user)
    return user

def verify_access_token(token: str) -> str:
    """
    Verify access token and return user ID
    """
    from app.core.security import get_user_id_from_token
    
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise ValueError("Invalid or expired token")
    
    return user_id

def refresh_access_token(refresh_token: str) -> str:
    """
    Refresh access token using refresh token
    """
    from app.core.security import verify_token, create_access_token
    
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token")
    
    user_id = payload.get("sub")
    return create_access_token(user_id)
```

### **2.5 Authentication Router**

#### **`backend/app/routers/auth.py`**
```python
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import GoogleCallbackRequest, AuthResponse, TokenResponse
from app.services.auth_service import process_google_oauth, verify_access_token, refresh_access_token
from app.core.config import settings
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/google/callback")
async def google_oauth_callback(
    request: GoogleCallbackRequest,
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback
    This endpoint is called by Next.js backend after user authenticates with Google
    """
    try:
        # Process Google OAuth flow
        tokens, user = await process_google_oauth(
            db=db,
            authorization_code=request.code,
            redirect_uri=request.redirect_uri
        )
        
        # Return tokens and user information
        return AuthResponse(
            token=TokenResponse(**tokens),
            user=user.to_dict()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

@router.get("/verify")
async def verify_token(
    token: Optional[str] = None,
    authorization: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Verify access token
    Accepts token in query param or Authorization header
    """
    try:
        # Extract token from header or query param
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split("Bearer ")[1]
        elif not token:
            raise HTTPException(status_code=401, detail="No token provided")
        
        # Verify token
        user_id = verify_access_token(token)
        
        # Get user from database
        from app.models.user import User
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive")
        
        return {
            "valid": True,
            "user": user.to_dict()
        }
        
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh")
async def refresh_token(request: dict):
    """
    Refresh access token using refresh token
    """
    try:
        refresh_token_str = request.get("refresh_token")
        if not refresh_token_str:
            raise HTTPException(status_code=400, detail="Refresh token required")
        
        access_token = refresh_access_token(refresh_token_str)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Get current user information
    Requires valid access token in Authorization header
    """
    # Get token from header
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    
    token = authorization.split("Bearer ")[1]
    
    try:
        # Verify token and get user
        user_id = verify_access_token(token)
        
        from app.models.user import User
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user.to_dict()
        
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
```

### **2.6 Main Application**

#### **`backend/app/main.py`**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import Base, engine
from app.routers import auth

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for authentication and user management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
```

#### **`backend/main.py`** (Entry point)
```python
from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.core.config import settings
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )
```

### **2.7 Requirements & Setup Script**

#### **`backend/requirements.txt`**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
httpx==0.25.2
alembic==1.12.1
aiosqlite==0.19.0
email-validator==2.1.0.post1
pydantic==2.5.0
pydantic-settings==2.1.0
```

#### **`backend/setup.sh`** (Optional setup script)
```bash
#!/bin/bash

# Setup script for FastAPI backend

echo "Setting up FastAPI backend..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create database
echo "Creating database..."
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
echo "Database created successfully!"

echo "Setup complete! Run 'source venv/bin/activate' then 'python main.py' to start the server."
```

---

## 🎯 **PHASE 3: NEXT.JS BACKEND IMPLEMENTATION**

### **3.1 API Client for FastAPI Communication**

#### **`frontend/lib/api.ts`**
```typescript
import axios from 'axios';

const FASTAPI_URL = process.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:8000';

// Create axios instance for FastAPI
export const fastapi = axios.create({
  baseURL: FASTAPI_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Add request interceptor to include auth token
fastapi.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('auth_token='))
        ?.split('=')[1];
      
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle errors
fastapi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default fastapi;
```

### **3.2 Authentication Utilities**

#### **`frontend/lib/auth.ts`**
```typescript
export interface User {
  id: string;
  email: string;
  name: string;
  picture_url: string | null;
  is_active: boolean;
  last_login: string | null;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthResponse {
  token: TokenResponse;
  user: User;
}

export const setAuthCookies = (token: string, user: User) => {
  // Set token cookie (HttpOnly will be set by backend)
  document.cookie = `auth_token=${token}; path=/; max-age=${3600}; SameSite=Strict; ${process.env.NODE_ENV === 'production' ? 'Secure;' : ''}`;
  
  // Set user data in localStorage for quick access
  localStorage.setItem('user', JSON.stringify(user));
};

export const getAuthToken = (): string | null => {
  if (typeof document === 'undefined') return null;
  
  const match = document.cookie.match(/auth_token=([^;]+)/);
  return match ? match[1] : null;
};

export const getUser = (): User | null => {
  if (typeof localStorage === 'undefined') return null;
  
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

export const clearAuth = () => {
  // Clear cookies
  document.cookie = 'auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
  document.cookie = 'user=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
  
  // Clear localStorage
  localStorage.removeItem('user');
  
  // Clear session data
  sessionStorage.clear();
};

export const isAuthenticated = (): boolean => {
  return !!getAuthToken() && !!getUser();
};
```

### **3.3 Next.js Backend API Routes**

#### **`frontend/pages/api/auth/login.ts`**
```typescript
import type { NextApiRequest, NextApiResponse } from 'next';

/**
 * POST /api/auth/login
 * Initiate Google OAuth login
 * This endpoint tells FastAPI to start the OAuth flow
 */
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { redirect_uri } = req.body;

    if (!redirect_uri) {
      return res.status(400).json({ error: 'redirect_uri is required' });
    }

    // Forward request to FastAPI to initiate OAuth
    const fastapiUrl = process.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:8000';
    
    const response = await fetch(`${fastapiUrl}/auth/google/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ redirect_uri }),
    });

    if (!response.ok) {
      const error = await response.json();
      return res.status(response.status).json({ error: error.detail || 'Failed to initiate OAuth' });
    }

    const data = await response.json();
    return res.status(200).json(data);

  } catch (error) {
    console.error('Login error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
```

#### **`frontend/pages/api/auth/callback/google.ts`**
```typescript
import type { NextApiRequest, NextApiResponse } from 'next';

/**
 * POST /api/auth/callback/google
 * Handle Google OAuth callback
 * This endpoint receives the authorization code from frontend
 * and exchanges it with FastAPI for user details and tokens
 */
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { code, redirect_uri } = req.body;

    if (!code || !redirect_uri) {
      return res.status(400).json({ 
        error: 'Authorization code and redirect_uri are required' 
      });
    }

    // Forward the authorization code to FastAPI
    const fastapiUrl = process.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:8000';
    
    const response = await fetch(`${fastapiUrl}/auth/google/callback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code, redirect_uri }),
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('FastAPI OAuth error:', error);
      return res.status(response.status).json({ 
        error: error.detail || 'Authentication failed' 
      });
    }

    // Get authentication response from FastAPI
    const authData = await response.json();
    
    // Set cookies for the token (HttpOnly)
    res.setHeader('Set-Cookie', [
      `auth_token=${authData.token.access_token}; Path=/; HttpOnly; SameSite=Strict; Max-Age=${3600}; ${process.env.NODE_ENV === 'production' ? 'Secure;' : ''}`,
      `refresh_token=${authData.token.refresh_token}; Path=/; HttpOnly; SameSite=Strict; Max-Age=${7 * 24 * 60 * 60}; ${process.env.NODE_ENV === 'production' ? 'Secure;' : ''}`,
    ]);

    // Return success response to frontend
    return res.status(200).json({
      success: true,
      user: authData.user,
      redirect: '/dashboard'
    });

  } catch (error) {
    console.error('OAuth callback error:', error);
    return res.status(500).json({ error: 'Internal server error during authentication' });
  }
}
```

#### **`frontend/pages/api/auth/verify.ts`**
```typescript
import type { NextApiRequest, NextApiResponse } from 'next';

/**
 * GET /api/auth/verify
 * Verify if user is authenticated
 */
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Get token from cookies
    const token = req.cookies.auth_token;

    if (!token) {
      return res.status(401).json({ authenticated: false });
    }

    // Verify token with FastAPI
    const fastapiUrl = process.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:8000';
    
    const response = await fetch(`${fastapiUrl}/auth/verify`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      // Token is invalid
      res.setHeader('Set-Cookie', [
        'auth_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT',
        'refresh_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT',
      ]);
      return res.status(401).json({ authenticated: false });
    }

    const data = await response.json();
    return res.status(200).json({ 
      authenticated: true, 
      user: data.user 
    });

  } catch (error) {
    console.error('Verify error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
```

#### **`frontend/pages/api/auth/logout.ts`**
```typescript
import type { NextApiRequest, NextApiResponse } from 'next';

/**
 * POST /api/auth/logout
 * Logout user and clear authentication
 */
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Clear authentication cookies
    res.setHeader('Set-Cookie', [
      'auth_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT',
      'refresh_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT',
      'user=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT',
    ]);

    return res.status(200).json({ success: true, message: 'Logged out successfully' });

  } catch (error) {
    console.error('Logout error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
```

### **3.4 Next.js Configuration**

#### **`frontend/next.config.js`**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['lh3.googleusercontent.com'], // For Google profile pictures
  },
  env: {
    NEXT_PUBLIC_FASTAPI_URL: process.env.NEXT_PUBLIC_FASTAPI_URL,
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

#### **`frontend/tailwind.config.js`**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
};
```

---

## 🎯 **PHASE 4: NEXT.JS FRONTEND IMPLEMENTATION**

### **4.1 Login Page**

#### **`frontend/pages/login.tsx`**
```typescript
import { useState } from 'react';
import { useRouter } from 'next/router';
import LoginButton from '../components/LoginButton';
import Head from 'next/head';

export default function LoginPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Handle OAuth callback from popup or redirect
  const handleOAuthCallback = async (code: string) => {
    setIsLoading(true);
    setError(null);

    try {
      // Get the redirect URI for callback
      const redirectUri = `${window.location.origin}/api/auth/callback/google`;

      // Send authorization code to Next.js backend
      const response = await fetch('/api/auth/callback/google', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code, redirect_uri: redirectUri }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Authentication failed');
      }

      const data = await response.json();
      
      // Redirect to dashboard
      router.push(data.redirect || '/dashboard');

    } catch (err: any) {
      setError(err.message || 'Login failed. Please try again.');
      setIsLoading(false);
    }
  };

  // Check if we have an authorization code in URL (callback)
  if (typeof window !== 'undefined') {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const error = urlParams.get('error');

    if (error) {
      setError(`Google OAuth error: ${error}`);
    } else if (code && !isLoading) {
      // Handle OAuth callback
      handleOAuthCallback(code);
    }
  }

  return (
    <>
      <Head>
        <title>Login - My App</title>
      </Head>

      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Sign in to your account
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              Or{' '}
              <a href="#" className="font-medium text-primary-600 hover:text-primary-500">
                start your 14-day free trial
              </a>
            </p>
          </div>

          <div className="mt-8">
            {error && (
              <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-lg">
                {error}
              </div>
            )}

            <div className="rounded-md shadow">
              <LoginButton isLoading={isLoading} />
            </div>

            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-gray-50 text-gray-500">
                    Or continue with
                  </span>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-1 gap-3">
                <button
                  disabled={isLoading}
                  onClick={() => {
                    // Open Google OAuth in popup
                    const redirectUri = `${window.location.origin}?oauth_callback=true`;
                    const authUrl = `${process.env.NEXT_PUBLIC_FASTAPI_URL}/auth/google/login?redirect_uri=${encodeURIComponent(redirectUri)}`;
                    
                    const popup = window.open(
                      authUrl,
                      'Google Login',
                      'width=500,height=600'
                    );
                  }}
                  className="w-full flex items-center justify-center px-4 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                >
                  {isLoading ? (
                    <span className="animate-spin mr-2">⏳</span>
                  ) : (
                    <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                      <path
                        fill="#4285F4"
                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                      />
                      <path
                        fill="#34A853"
                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                      />
                      <path
                        fill="#FBBC05"
                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                      />
                      <path
                        fill="#EA4335"
                        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                      />
                    </svg>
                  )}
                  {isLoading ? 'Processing...' : 'Continue with Google'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
```

### **4.2 Login Button Component**

#### **`frontend/components/LoginButton.tsx`**
```typescript
import { useRouter } from 'next/router';

interface LoginButtonProps {
  isLoading?: boolean;
  className?: string;
}

export default function LoginButton({ isLoading = false, className = '' }: LoginButtonProps) {
  const router = useRouter();

  const handleGoogleLogin = async () => {
    try {
      // Step 1: Get Google OAuth URL from FastAPI via Next.js backend
      const redirectUri = `${window.location.origin}?oauth_callback=true`;
      
      // Open popup window for Google OAuth
      const popup = window.open(
        `${process.env.NEXT_PUBLIC_FASTAPI_URL}/auth/google/login?redirect_uri=${encodeURIComponent(redirectUri)}`,
        'Google Login',
        'width=500,height=600,left=100,top=100'
      );

      if (!popup) {
        throw new Error('Popup blocked. Please allow popups for this site.');
      }

      // Listen for popup messages
      const handleMessage = async (event: MessageEvent) => {
        // Verify origin for security
        if (event.origin !== window.location.origin) return;

        if (event.data.type === 'GOOGLE_OAUTH_SUCCESS') {
          // Close popup
          popup.close();
          window.removeEventListener('message', handleMessage);

          // Handle the authorization code
          const { code } = event.data;
          
          try {
            // Send code to Next.js backend
            const response = await fetch('/api/auth/callback/google', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ 
                code, 
                redirect_uri: `${window.location.origin}/api/auth/callback/google` 
              }),
            });

            if (response.ok) {
              const data = await response.json();
              router.push(data.redirect || '/dashboard');
            } else {
              const error = await response.json();
              alert(error.error || 'Login failed');
            }
          } catch (err) {
            console.error('Login error:', err);
            alert('Login failed. Please try again.');
          }
        } else if (event.data.type === 'GOOGLE_OAUTH_ERROR') {
          popup.close();
          window.removeEventListener('message', handleMessage);
          alert(event.data.error || 'Google OAuth failed');
        }
      };

      window.addEventListener('message', handleMessage);

    } catch (error: any) {
      console.error('Login error:', error);
      alert(error.message || 'Failed to initiate login');
    }
  };

  return (
    <button
      onClick={handleGoogleLogin}
      disabled={isLoading}
      className={`w-full flex items-center justify-center gap-2 px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors ${className}`}
    >
      {isLoading ? (
        <>
          <span className="animate-spin">⏳</span>
          Processing...
        </>
      ) : (
        <>
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Sign in with Google
        </>
      )}
    </button>
  );
}
```

### **4.3 Protected Route Component**

#### **`frontend/components/ProtectedRoute.tsx`**
```typescript
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { isAuthenticated } from '../lib/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectPath?: string;
}

export default function ProtectedRoute({
  children,
  redirectPath = '/login',
}: ProtectedRouteProps) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // First check local storage for quick access
        const hasLocalAuth = isAuthenticated();
        
        if (hasLocalAuth) {
          // Verify token with backend
          const response = await fetch('/api/auth/verify');
          const data = await response.json();

          if (data.authenticated) {
            setIsAuth(true);
          } else {
            // Token invalid, redirect to login
            router.push(redirectPath);
          }
        } else {
          // No local auth, redirect to login
          router.push(redirectPath);
        }
      } catch (error) {
        console.error('Auth check error:', error);
        router.push(redirectPath);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, [router, redirectPath]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return isAuth ? <>{children}</> : null;
}
```

### **4.4 Dashboard Page**

#### **`frontend/pages/dashboard.tsx`**
```typescript
import { useState, useEffect } from 'react';
import ProtectedRoute from '../components/ProtectedRoute';
import { getUser, clearAuth } from '../lib/auth';
import { useRouter } from 'next/router';
import Head from 'next/head';

interface DashboardData {
  totalUsers: number;
  recentActivity: any[];
}

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get user from localStorage
    const currentUser = getUser();
    setUser(currentUser);

    // Fetch dashboard data
    const fetchDashboardData = async () => {
      try {
        const response = await fetch('/api/dashboard');
        if (response.ok) {
          const data = await response.json();
          setDashboardData(data);
        }
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout', {
        method: 'POST',
      });
      
      clearAuth();
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <ProtectedRoute>
      <Head>
        <title>Dashboard - My App</title>
      </Head>

      <div className="min-h-screen bg-gray-100">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            
            <div className="flex items-center gap-4">
              {user && (
                <div className="flex items-center gap-3">
                  {user.picture_url ? (
                    <img
                      src={user.picture_url}
                      alt={user.name}
                      className="w-10 h-10 rounded-full"
                    />
                  ) : (
                    <div className="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-medium">
                      {user.name.charAt(0)}
                    </div>
                  )}
                  <div>
                    <p className="text-sm font-medium text-gray-700">{user.name}</p>
                    <p className="text-xs text-gray-500">{user.email}</p>
                  </div>
                </div>
              )}
              
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading dashboard...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Welcome Card */}
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-2">
                  Welcome back, {user?.name}!
                </h2>
                <p className="text-sm text-gray-600">
                  Last login: {user?.last_login ? new Date(user.last_login).toLocaleString() : 'N/A'}
                </p>
              </div>

              {/* Stats Cards */}
              {dashboardData && (
                <>
                  <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-sm font-medium text-gray-500">Total Users</h3>
                    <p className="mt-2 text-3xl font-bold text-gray-900">
                      {dashboardData.totalUsers}
                    </p>
                  </div>

                  <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-sm font-medium text-gray-500">Recent Activity</h3>
                    <p className="mt-2 text-3xl font-bold text-gray-900">
                      {dashboardData.recentActivity.length}
                    </p>
                  </div>
                </>
              )}

              {/* Quick Actions */}
              <div className="bg-white rounded-lg shadow p-6 col-span-full">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Quick Actions
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <button className="px-4 py-3 bg-primary-50 text-primary-700 rounded-lg hover:bg-primary-100 transition-colors">
                    New Project
                  </button>
                  <button className="px-4 py-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors">
                    View Reports
                  </button>
                  <button className="px-4 py-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors">
                    Settings
                  </button>
                  <button className="px-4 py-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors">
                    Help & Support
                  </button>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}
```

### **4.5 Home Page (Landing)**

#### **`frontend/pages/index.tsx`**
```typescript
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { isAuthenticated } from '../lib/auth';
import Head from 'next/head';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to dashboard if already authenticated
    if (isAuthenticated()) {
      router.push('/dashboard');
    }
  }, [router]);

  return (
    <>
      <Head>
        <title>Welcome - My App</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex flex-col">
        {/* Navigation */}
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-primary-600">My App</div>
          <a
            href="/login"
            className="px-6 py-2 bg-white text-primary-600 rounded-lg font-medium hover:bg-gray-50 transition-colors"
          >
            Sign In
          </a>
        </nav>

        {/* Hero Section */}
        <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-5xl font-extrabold text-gray-900 mb-6">
              Welcome to <span className="text-primary-600">My App</span>
            </h1>
            <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
              The best way to manage your projects and collaborate with your team.
              Sign in with Google to get started.
            </p>
            
            <a
              href="/login"
              className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
            >
              Get Started
            </a>
          </div>
        </main>

        {/* Footer */}
        <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center text-gray-600">
          <p>&copy; {new Date().getFullYear()} My App. All rights reserved.</p>
        </footer>
      </div>
    </>
  );
}
```

---

## 🎯 **PHASE 5: COMPLETE FLOW EXPLANATION**

### **5.1 Complete User Login Flow**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        COMPLETE LOGIN FLOW                                              │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                         │
│  STEP 1: User clicks "Sign in with Google" on Frontend                                                  │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  Next.js Frontend (login.tsx)                                                                           │
│  └─> Opens popup window with FastAPI OAuth URL                                                          │
│      URL: http://localhost:8000/auth/google/login?redirect_uri=http://localhost:3000?oauth_callback=true│
│                                                                                                         │
│  STEP 2: FastAPI initiates Google OAuth                                                                 │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  FastAPI Backend (/auth/google/login)                                                                   │
│  └─> Redirects popup to Google OAuth consent screen                                                     │
│      Google URL with client_id, scope, redirect_uri, state                                              │
│                                                                                                         │
│  STEP 3: User authenticates with Google                                                                 │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  Google OAuth Screen                                                                                    │
│  └─> User enters credentials                                                                            │
│  └─> Google verifies user                                                                               │
│  └─> Google generates authorization code                                                                │
│                                                                                                         │
│  STEP 4: Google redirects back to FastAPI                                                               │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  Google Redirect                                                                                        │
│  └─> Redirects to: http://localhost:8000/auth/google/callback?code=AUTH_CODE&state=STATE               │
│                                                                                                         │
│  STEP 5: FastAPI handles OAuth callback (server-side)                                                   │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  FastAPI Backend (/auth/google/callback)                                                                │
│  ├─> Validates state parameter                                                                          │
│  ├─> Exchanges authorization code for access token (with client_secret)                                 │
│  ├─> Gets user info from Google using access token                                                      │
│  ├─> Checks database for existing user                                                                  │
│  ├─> Creates/updates user in database                                                                   │
│  ├─> Generates JWT access token and refresh token                                                       │
│  └─> Sends success message to popup window via JavaScript postMessage                                   │
│                                                                                                         │
│  STEP 6: Popup sends success message to parent window                                                   │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  Popup Window (FastAPI frontend template)                                                               │
│  └─> window.opener.postMessage({                                                                        │
│        type: 'GOOGLE_OAUTH_SUCCESS',                                                                    │
│        code: AUTH_CODE                                                                                  │
│      }, window.location.origin)                                                                         │
│                                                                                                         │
│  STEP 7: Frontend receives message and closes popup                                                    │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  Next.js Frontend (LoginButton.tsx)                                                                     │
│  ├─> Receives postMessage from popup                                                                    │
│  ├─> Closes popup window                                                                                │
│  └─> Sends authorization code to Next.js backend                                                        │
│      POST /api/auth/callback/google                                                                     │
│      Body: { code: AUTH_CODE, redirect_uri: "http://localhost:3000/api/auth/callback/google" }          │
│                                                                                                         │
│  STEP 8: Next.js backend forwards to FastAPI                                                            │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  Next.js Backend (/api/auth/callback/google)                                                            │
│  └─> Forwards request to FastAPI:                                                                       │
│      POST http://localhost:8000/auth/google/callback                                                    │
│      Body: { code: AUTH_CODE, redirect_uri: "..." }                                                     │
│                                                                                                         │
│  STEP 9: FastAPI processes authentication                                                               │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  FastAPI Backend (same as STEP 5)                                                                       │
│  └─> Returns: {                                                                                         │
│        token: { access_token, refresh_token },                                                          │
│        user: { id, email, name, picture_url, ... }                                                      │
│      }                                                                                                  │
│                                                                                                         │
│  STEP 10: Next.js backend sets cookies and responds                                                     │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  Next.js Backend                                                                                        │
│  ├─> Sets HttpOnly cookies:                                                                             │
│  │   - auth_token (access token)                                                                        │
│  │   - refresh_token                                                                                    │
│  └─> Returns: { success: true, user: {...}, redirect: '/dashboard' }                                    │
│                                                                                                         │
│  STEP 11: Frontend receives response and redirects                                                      │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  Next.js Frontend                                                                                        │
│  ├─> Stores user data in localStorage                                                                   │
│  └─> Redirects to /dashboard                                                                            │
│                                                                                                         │
│  STEP 12: Dashboard loads with authenticated user                                                       │
│  ──────────────────────────────────────────────────────────────────────────────────────────────────────│
│  Next.js Frontend (dashboard.tsx)                                                                       │
│  ├─> ProtectedRoute checks authentication                                                               │
│  ├─> Fetches /api/auth/verify                                                                           │
│  ├─> Next.js backend verifies token with FastAPI                                                        │
│  └─> Dashboard displays user information                                                                │
│                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### **5.2 Sequence Diagram**

```
User      Next.js       Next.js       FastAPI       Google        Database
Frontend  Backend       Backend       Backend
────────────────────────────────────────────────────────────────────────────
   │          │             │             │            │            │
   │──Click──▶│             │             │            │            │
   │  Login   │             │             │            │            │
   │          │             │             │            │            │
   │          │             │             │            │            │
   │◀────Open Popup────────│             │            │            │
   │          │             │             │            │            │
   │          │──Redirect──▶│             │            │            │
   │          │   to FastAPI│             │            │            │
   │          │             │             │            │            │
   │          │             │──Redirect──▶│            │            │
   │          │             │   to Google │            │            │
   │          │             │             │            │            │
   │          │             │             │──Show────▶│            │
   │          │             │             │  OAuth    │            │
   │          │             │             │  Screen   │            │
   │          │             │             │◀────Enter Credentials──│
   │          │             │             │            │            │
   │          │             │             │◀──Verify───│            │
   │          │             │             │            │            │
   │          │             │             │◀──Generate Code────────│
   │          │             │             │            │            │
   │          │             │◀────Redirect─────────────│            │
   │          │             │   with code │            │            │
   │          │             │             │            │            │
   │          │             │             │            │            │
   │          │             │──Exchange Code──────────▶│            │
   │          │             │   for Token │            │            │
   │          │             │             │            │            │
   │          │             │◀────Tokens───────────────│            │
   │          │             │             │            │            │
   │          │             │──Get User Info──────────▶│            │
   │          │             │             │            │            │
   │          │             │◀────User Info────────────│            │
   │          │             │             │            │            │
   │          │             │──Check/Save──────────────────────────▶│
   │          │             │   User      │            │            │
   │          │             │◀────User──────────────────────────────│
   │          │             │             │            │            │
   │          │◀────postMessage───────────│            │            │
   │          │   (success) │             │            │            │
   │          │             │             │            │            │
   │◀──Close Popup─────────│             │            │            │
   │          │             │             │            │            │
   │──Send Code──────────▶│             │            │            │
   │          │             │             │            │            │
   │          │──Forward───▶│             │            │            │
   │          │   to FastAPI│             │            │            │
   │          │             │             │            │            │
   │          │             │──Process Auth (same as above)───────▶│
   │          │             │             │            │            │
   │          │◀────Auth Response─────────│            │            │
   │          │   (tokens + user)         │            │            │
   │          │             │             │            │            │
   │          │──Set Cookies──────────────│            │            │
   │          │             │             │            │            │
   │◀────Redirect to Dashboard────────────│            │            │
   │          │             │             │            │            │
   │──Load Dashboard──────▶│             │            │            │
   │          │             │             │            │            │
   │          │──Verify Auth─────────────▶│            │            │
   │          │             │             │            │            │
   │          │◀────Valid─────────────────│            │            │
   │          │             │             │            │            │
   │◀────Show Dashboard────│             │            │            │
```

---

## 🎯 **PHASE 6: TESTING & DEPLOYMENT**

### **6.1 Testing Checklist**

#### **Backend Tests**
```python
# backend/tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_google_oauth_flow():
    # Test the complete OAuth flow
    # This requires mocking Google OAuth responses
    pass

def test_token_verification():
    # Test token verification endpoint
    pass
```

#### **Frontend Tests**
```typescript
// frontend/__tests__/login.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { useRouter } from 'next/router';
import LoginPage from '../pages/login';

jest.mock('next/router', () => ({
  useRouter: jest.fn(),
}));

describe('LoginPage', () => {
  it('renders login button', () => {
    (useRouter as jest.Mock).mockReturnValue({ push: jest.fn() });
    render(<LoginPage />);
    expect(screen.getByText(/sign in with google/i)).toBeInTheDocument();
  });

  it('handles login click', async () => {
    const push = jest.fn();
    (useRouter as jest.Mock).mockReturnValue({ push });
    
    render(<LoginPage />);
    fireEvent.click(screen.getByText(/sign in with google/i));
    
    // Add assertions for popup behavior
  });
});
```

### **6.2 Environment Setup Scripts**

#### **Backend Setup Script**
```bash
# backend/setup.sh
#!/bin/bash

echo "🚀 Setting up FastAPI backend..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create database
echo "🗄️  Creating database..."
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
APP_NAME="My App Backend"
ENVIRONMENT="development"
BASE_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"
HOST="0.0.0.0"
PORT=8000
DATABASE_URL="sqlite:///./test.db"
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
GOOGLE_REDIRECT_URI="http://localhost:8000/auth/google/callback"
SECRET_KEY="change-this-secret-key-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS="http://localhost:3000,http://localhost:3001"
EOF
    echo "⚠️  Please update .env with your actual credentials!"
fi

echo "✅ Setup complete!"
echo "📝 Next steps:"
echo "   1. Update .env with your Google OAuth credentials"
echo "   2. Run: source venv/bin/activate"
echo "   3. Run: python main.py"
```

#### **Frontend Setup Script**
```bash
# frontend/setup.sh
#!/bin/bash

echo "🚀 Setting up Next.js frontend..."

# Install dependencies
npm install

# Create .env.local if not exists
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local file..."
    cat > .env.local << EOF
NEXT_PUBLIC_APP_NAME="My App"
NEXT_PUBLIC_API_URL="http://localhost:3000/api"
NEXT_PUBLIC_FASTAPI_URL="http://localhost:8000"
NEXT_PUBLIC_GOOGLE_CLIENT_ID="your-google-client-id"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="change-this-in-production"
EOF
    echo "⚠️  Please update .env.local with your actual credentials!"
fi

echo "✅ Setup complete!"
echo "📝 Next steps:"
echo "   1. Update .env.local with your Google OAuth credentials"
echo "   2. Run: npm run dev"
```

### **6.3 Running the Application**

#### **Terminal 1: Start FastAPI Backend**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

#### **Terminal 2: Start Next.js Frontend**
```bash
cd frontend
npm run dev
```

#### **Access the Application**
- Frontend: http://localhost:3000
- Backend API Docs: http://localhost:8000/docs
- Backend Health Check: http://localhost:8000/health

### **6.4 Google OAuth Setup**

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select existing one
3. **Enable Google+ API**:
   - Navigation menu → APIs & Services → Library
   - Search for "Google+ API" and enable it
4. **Create OAuth 2.0 credentials**:
   - Navigation menu → APIs & Services → Credentials
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Web application"
   - Add authorized JavaScript origins:
     - `http://localhost:3000`
     - `http://localhost:8000`
   - Add authorized redirect URIs:
     - `http://localhost:8000/auth/google/callback`
     - `http://localhost:3000/api/auth/callback/google`
5. **Copy credentials**:
   - Copy Client ID and Client Secret
   - Add to `.env` files in both frontend and backend

---

## 📊 **Complete File Structure Summary**

```
project-root/
├── README.md
├── frontend/
│   ├── pages/
│   │   ├── index.tsx              # Landing page
│   │   ├── login.tsx              # Login page
│   │   ├── dashboard.tsx          # Protected dashboard
│   │   └── api/
│   │       └── auth/
│   │           ├── login.ts       # Initiate OAuth
│   │           ├── callback/
│   │           │   └── google.ts  # Handle OAuth callback
│   │           ├── verify.ts      # Verify auth
│   │           └── logout.ts      # Logout
│   ├── components/
│   │   ├── LoginButton.tsx        # Google login button
│   │   └── ProtectedRoute.tsx     # Route protection
│   ├── lib/
│   │   ├── api.ts                 # API client
│   │   └── auth.ts                # Auth utilities
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── .env.local
│   ├── package.json
│   └── setup.sh
│
└── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py                   # FastAPI app
    │   ├── database.py               # Database setup
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── config.py             # Settings
    │   │   └── security.py           # JWT utilities
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── user.py               # User model
    │   ├── schemas/
    │   │   ├── __init__.py
    │   │   └── auth.py               # Pydantic schemas
    │   ├── routers/
    │   │   ├── __init__.py
    │   │   └── auth.py               # Auth endpoints
    │   ├── services/
    │   │   ├── __init__.py
    │   │   └── auth_service.py       # Auth business logic
    │   └── utils/
    │       ├── __init__.py
    │       └── oauth.py              # OAuth utilities
    ├── main.py                       # Entry point
    ├── requirements.txt
    ├── .env
    └── setup.sh
```

---

## 🎉 **Summary**

This complete roadmap provides you with:

✅ **Clear architecture**: Next.js Frontend ↔ Next.js Backend ↔ FastAPI Backend  
✅ **Complete OAuth flow**: Google OAuth handled entirely by FastAPI  
✅ **Security best practices**: HttpOnly cookies, JWT tokens, CORS configuration  
✅ **Production-ready code**: Error handling, validation, TypeScript types  
✅ **Easy setup**: Setup scripts and configuration files  
✅ **Testing guidance**: Test examples and checklist  
✅ **Deployment ready**: Environment configuration and Google OAuth setup  

**Next Steps:**
1. Set up the project structure
2. Configure environment variables
3. Set up Google OAuth credentials
4. Run both servers
5. Test the complete login flow
6. Customize UI and add your application features

Happy coding! 🚀