from fastapi import APIRouter, Depends

from app.schemas.admin import AdminLoginRequest, TokenResponse
from app.utils.auth import authenticate_admin, create_access_token

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login", response_model=TokenResponse)
def admin_login(credentials: AdminLoginRequest):
    if not authenticate_admin(credentials.username, credentials.password):
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token({"sub": credentials.username, "role": "admin"})
    return TokenResponse(access_token=token)
