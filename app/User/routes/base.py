from typing import Annotated

from fastapi import APIRouter, Body

from app.common.annotations import DatabaseSession
from app.common.auth import AuthJWTGen
from app.common.schemas import ResponseSchema
from app.core.settings import get_settings
from app.User import selectors, services
from app.User.annotations import CurrentUser
from app.User.crud import UserRefreshTokenCRUD
from app.User.schemas import base, create, response
from app.User import formatters


# Globals
router = APIRouter()
settings = get_settings()
token_gen = AuthJWTGen()


#####################################################################
# BASE
#####################################################################
@router.post(
    "",
    summary="Create a new user",
    response_description="The created user's data",
    status_code=200,
    response_model=response.UserResponse,
)
async def route_create_user(user_in: create.UserCreate, db: DatabaseSession):
    """
    This endpoint creates a user
    """

    # Create the user
    user = await services.create_user(data=user_in, db=db)

    return {"data": await formatters.format_user(user)}


#####################################################################
# AUTH
#####################################################################
@router.post(
    "/login",
    summary="Login User",
    response_description="The user's access token",
    status_code=200,
    response_model=response.UserLoginResponse,
)
async def route_user_login(cred_in: base.UserLoginCredential, db: DatabaseSession):
    """
    This endpoint logs in a user
    """

    # Login User
    user = await services.login_user(data=cred_in, db=db)

    # Generate refresh token
    ref_token = await services.create_user_refresh_token(user=user, db=db)

    # Generate access token
    access_token = await token_gen.create_token(
        subject=f"USER-{user.id}",
        type_token="access",
        ref_id=ref_token.id,
        issuer="AyriaTech.com"
    )

    await db.commit()

    return {
        "data": {
            "user": await formatters.format_user(user),
            "tokens": {"access_token": access_token, "refresh_token": ref_token.token},
        }
    }


@router.post(
    "/token",
    summary="Refreshes User Tokens",
    response_description="The new user token",
    status_code=200,
    response_model=response.UserLoginResponse,
)
async def route_user_token(
    token: Annotated[str, Body(embed=True, description="The user's refresh token")],
    db: DatabaseSession,
):
    """
    This endpoint refreshes the user's token
    """

    # Verify refresh token
    ref_token = await selectors.get_user_refresh_token(token=token, db=db)

    # Generate access token
    access_token = await token_gen.create_token(
        subject=f"USER-{ref_token.user_id}",
        type_token="access",
        ref_id=ref_token.id,
        issuer="AyriaTech.com"
    )

    return {
        "data": {
            "user": await formatters.format_user(
                # NOTE: this should never return None
                user=await selectors.get_user_by_id(id=ref_token.user_id, db=db)  # type: ignore
            ),
            "tokens": {"access_token": access_token, "refresh_token": ref_token.token},
        }
    }


@router.delete(
    "/logout",
    summary="User logout",
    response_description="The logout response",
    status_code=200,
    response_model=ResponseSchema,
)
async def route_user_logout(curr_user: CurrentUser, db: DatabaseSession):
    """
    This endpoint logs out a user
    """

    # Init crud
    ref_token_crud = UserRefreshTokenCRUD(db=db)

    # Deactivate refresh tokens
    await ref_token_crud.delete_tokens(user=curr_user)

    return {
        "data": {
            "msg": "User logged out sucessfully",
        }
    }


@router.get(
    "/me",
    summary="Get Authenticated User",
    response_description="The User profile response",
    status_code=200,
    response_model=response.UserResponse,
)
async def route_user_profile(curr_user: CurrentUser, db: DatabaseSession):
    """
    This endpoint displays the current user's profile
    """

    user = await selectors.get_user_by_id(id=curr_user.id, db=db)

    return {"data": await formatters.format_user(user)}
