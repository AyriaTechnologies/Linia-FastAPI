from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.annotations import DatabaseSession
from app.User.crud import UserCRUD, UserRefreshTokenCRUD
from app.User.exceptions import UserNotFound
from app.common.auth import AuthJWTGen
from app.common.exceptions import Forbidden, Unauthorized
from app.core.settings import get_settings

# Globals
settings = get_settings()
token_gen = AuthJWTGen()


async def get_user_by_id(
    id: int, db: AsyncSession, raise_exc: bool = True, return_active: bool = True
):
    """
    Get user obj based on the user's ID

    Args:
        id (int): The user's id
        db (AsyncSession): The database Session
        raise_exc (bool): Raises a 404 error if the user is not found. Defaults to True.
        return_disabled (bool = False)

    Raises:
        UserNotFound

    Returns:
        models.User: The user object
    """
    # init CRUD
    user_crud = UserCRUD(db=db)

    # get user by id
    user = await user_crud.get(id=id)

    # Check: user not found
    if not user and raise_exc:
        raise UserNotFound()

    # Check: inactive user
    if user and not bool(user.is_active) and return_active:
        raise Forbidden("User has been deactivated")

    return user


async def get_current_user(
    token: Annotated[str, Header(alias="Authorization")],
    db: DatabaseSession,
):
    """
    Returns Current user logged in

    Args:
        token (str): Authorization token.
        db (AsyncSession): The database session

    Raises:
        Unauthorized: Invalid Token
        ValueError: User ID cannot be None

    Returns:
        models.User: The user object
    """
    # Split token
    try:
        token = token.split()[1]

    except KeyError:
        raise Unauthorized("Invalid token")

    # Verify token
    user_id = await token_gen.verify(
        token=token, sub_head="USER", db=db, crud_class=UserRefreshTokenCRUD
    )

    # Check: valid user id
    user = await get_user_by_id(id=int(user_id), db=db)

    return user


async def get_user_refresh_token(token: str, db: AsyncSession):
    """
    Get user refresh token

    Args:
        token (str): The refresh
        db (AsyncSession): The database session

    Raises:
        Unauthorized: Refresh token not found
        Unauthorized: Refresh token has expired

    Returns:
        models.UserRefreshToken: The user's refresh token
    """
    # Init crud
    ref_token_crud = UserRefreshTokenCRUD(db=db)

    # Get ref token
    ref_token = await ref_token_crud.get(token=token)

    # Check: exists
    if not ref_token:
        raise Unauthorized("Refresh token not found")

    # Check: expired
    token_expires_at: datetime = ref_token.created_at + timedelta(
        hours=settings.REFRESH_TOKEN_EXPIRE_HOUR  # type: ignore
    )
    if datetime.now() > token_expires_at.replace(tzinfo=None):
        raise Unauthorized("Refresh token has expired")

    return ref_token
