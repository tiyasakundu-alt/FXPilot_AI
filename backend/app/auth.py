
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError

# Load environment variables from .env
load_dotenv()

# Password hashing configuration
password_hash = PasswordHash.recommended()

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY is missing from environment variables"
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 1. Hash user password
def hash_password(password: str) -> str:
    """Securely hash a user's password using Argon2."""
    return password_hash.hash(password)


# 2. Verify user password
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """Verify a plain password against its stored hash."""
    return password_hash.verify(
        plain_password,
        hashed_password
    )


# 3. Generate JWT access token
def create_access_token(subject: str) -> str:
    """Create a signed JWT access token."""
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# 4. Verify JWT access token
def verify_access_token(token: str) -> str:
    """Verify JWT and return the user's identity."""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        subject = payload.get("sub")

        if not subject:
            raise InvalidTokenError("Missing token subject")

        return subject

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"}
        )
