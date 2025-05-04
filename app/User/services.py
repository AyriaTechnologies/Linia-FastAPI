from sqlalchemy.ext.asyncio import AsyncSession
from app.User import models
from app.User.crud import UserCRUD, UserRefreshTokenCRUD
from app.User.schemas import base, create
from app.common.auth import AuthJWTGen
from app.common.exceptions import BadRequest, Unauthorized
from app.common.security import hash_password, verify_password

token_gen = AuthJWTGen()


async def create_user(data: create.UserCreate, db: AsyncSession):
    """
    Create a new user

    Args:
        data (create.UserCreate): The user's details
        db (AsyncSession): The database session

    Raises:
        BadRequest: User with email exist

    Returns:
        models.User: The created user obj
    """
    # Init CRUD
    user_crud = UserCRUD(db=db)

    # Check: if email exists
    if await user_crud.get(email=data.email):
        raise BadRequest(msg="User with email already exists")

    user = await user_crud.create(
        data={
            "password": await hash_password(raw=data.password),
            **data.model_dump(exclude={"password"}),
        }
    )

    return user


async def login_user(data: base.UserLoginCredential, db: AsyncSession):
    """
    Login user

    Args:
        data (base.UserLoginCredential): The user's login credentials
        db (Session): The database session

    Raises:
        Unauthorized

    Returns:
        models.User: The logged in user obj
    """

    # Init Crud
    user_crud = UserCRUD(db=db)

    # Get user obj
    obj = await user_crud.get(email=data.email)
    if not obj:
        raise Unauthorized("Invalid Login Credentials")

    # Verify password
    if not await verify_password(raw=data.password, hashed=obj.password):
        raise Unauthorized("Invalid Login Credentials")

    return obj


async def create_user_refresh_token(user: models.User, db: AsyncSession):
    """
    Creates a user refresh token

    Args:
        user (models.User): The user obj
        db (AsyncSession): The database session

    Returns:
        models.UserRefreshToken: The user refresh token obj
    """

    # Init Crud
    ref_token_crud = UserRefreshTokenCRUD(db=db)

    # create the ref token
    ref_token_obj = await ref_token_crud.create(
        data={
            "user_id": user.id,
            "token": await token_gen.create_token(subject=user.id, type_token="refresh"),
        }
    )

    return ref_token_obj
