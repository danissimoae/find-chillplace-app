from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import SECRET_KEY, ALGORITHM
from app.exceptions import TokenAbsentException, IncorrectTokenFormatException, TokenExpiredException, \
    UserIsNotPresentException
from app.users.data_access_object import Users_Data_Access_Object


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str  = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await Users_Data_Access_Object.select_one_or_none_filter_by(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user



