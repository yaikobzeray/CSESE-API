from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.db.session import DbSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_admin(token: TokenDep, db: DbSession):
    """Dependency that validates the JWT and returns the current admin user."""
    from app.crud.admin import get_admin_by_id
    from app.models.admin import Admin

    subject = decode_access_token(token)
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    admin: Admin | None = get_admin_by_id(db, int(subject))
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive admin account",
        )
    return admin


CurrentAdmin = Annotated[object, Depends(get_current_admin)]
