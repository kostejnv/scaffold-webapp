from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authorize(token: str = Depends(oauth2_scheme)):
    """Authorize the request."""
    settings = Settings()
    if token != settings.ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
