from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.user import TokenData, UserInDB
from app.utils.security import SECRET_KEY, ALGORITHM, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 模拟数据库
db = {
    "guinan": {
        "username": "guinan",
        "full_name": "Lin Guinan",
        "email": "goodhawk@gmail.com",
        "hashed_password": "$2b$12$DtuN0zzjDHhBOKhsUsxp2ua3wHvOR1Xj5OoqvqCCj48dk.XzRxt3i",
        "disabled": False
    }
}

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user 