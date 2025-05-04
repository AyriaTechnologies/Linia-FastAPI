from typing import Dict, Optional, Type, Union
from datetime import datetime, timedelta
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import Unauthorized
from app.core.settings import get_settings

settings = get_settings()


class AuthJWTGen:
    def __init__(self) -> None:
        self.secret_key = settings.USER_SECRET_KEY
        self.access_expire_in = settings.ACCESS_TOKEN_EXPIRE_MIN
        self.refresh_expire_in = settings.REFRESH_TOKEN_EXPIRE_HOUR

    async def create_token(
        self,
        subject: Union[str, int],
        type_token: str,
        ref_id: int | None = None,
        fresh: bool | None = False,
        algorithm: str | None = "HS256",
        headers: Dict | None = None,
        issuer: str | None = None,
        extra_claims: Dict | None = None,
    ):
        """
        Generate token for access_token and refresh_token (utf-8)

        Args:
            subject (Union[str, int]): Identifier for who this token is for.
            type_token (str): indicate token is access_token or refresh_token
            fresh: Optional when token is access_token this param required
            algorithm (Optional[str], optional): algorithm to encode the token. Defaults to "HS256".
            headers (Optional[Dict], optional): Defaults to None.
            issuer (Optional[str], optional): expected issuer in the JWT
            extra_claims: Custom claims to include in this token. This data must be dictionary

        Return: Encoded token
        """

        # Data Type Validation
        if not isinstance(subject, (str, int)):
            raise TypeError("subject must be a string or integer")
        if not isinstance(fresh, bool):
            raise TypeError("fresh must be a boolean")
        if type_token not in {"access", "refresh"}:
            raise ValueError("type_token must be 'access' or 'refresh'")

        iat = datetime.now()
        expire = iat + timedelta(
            minutes=self.access_expire_in
            if type_token == "access"
            else self.refresh_expire_in * 60
        )

        # Data section
        reserved_claims = {
            "sub": subject,
            "iat": int(iat.timestamp()),
            "exp": int(expire.timestamp()),
        }

        custom_claims = {"type": type_token}

        # for access_token only fresh needed
        if type_token == "access":
            custom_claims["fresh"] = fresh

        if ref_id:
            custom_claims["ref_id"] = str(ref_id)

        if issuer:
            custom_claims["iss"] = issuer

        if extra_claims is None:
            extra_claims = {}

        return jwt.encode(
            {**reserved_claims, **custom_claims, **extra_claims},
            key=self.secret_key,
            algorithm=algorithm,
            headers=headers,
        )

    async def verify_access_token(
        self, token: str, sub_head: str, algorithms: Optional[str] = "HS256"
    ) -> str:
        """
        Verifies the provided JWT token and checks its validity based on sub_head (prefix in 'sub' field).

        Args:
            token (str): The JWT token to verify.
            sub_head (str): Expected prefix of the 'sub' field in the token payload.

        Returns:
            str: The ID part of 'sub' if verification succeeds.

        Raises:
            Unauthorized: If the token is invalid or expired.
        """
        try:
            # Decode the token and extract the payload
            payload = jwt.decode(token, key=self.secret_key, algorithms=algorithms)

            # Extract and validate the 'sub' field
            sub: str = payload.get("sub")
            if not sub:
                raise Unauthorized("Invalid Token")

            # Ensure the token is of type 'access'
            if payload.get("type") != "access":
                raise Unauthorized("Token type is invalid")

            # Validate the 'sub' structure: sub should be prefixed with sub_head
            sub_parts = sub.split("-")
            if sub_parts[0] != sub_head or len(sub_parts) < 2:
                raise Unauthorized("Invalid Token")

            # Return the ID part of 'sub'
            return sub_parts[1]

        except jwt.ExpiredSignatureError:
            raise Unauthorized("Access Token has expired")
        except jwt.PyJWTError:
            raise Unauthorized("Invalid Token")

    async def verify_refresh_token(
        self, token: str, sub_head: str, algorithms: Optional[str] = "HS256"
    ) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=algorithms)
            if payload.get("type") != "refresh":
                raise Unauthorized(f"{sub_head}Token type is invalid")

            if payload.get("exp") and datetime.utcnow().timestamp() > payload["exp"]:
                raise Unauthorized(f"{sub_head}Token expired")

            return payload

        except jwt.PyJWTError:
            raise Unauthorized(f"{sub_head}Invalid token")

    async def verify(
        self, token: str, sub_head: str, db: AsyncSession, crud_class: Type
    ) -> str:
        """
        Verifies the provided JWT token using a generic CRUD class.

        Args:
            token (str): The JWT token to verify.
            sub_head (str): Expected prefix of the 'sub' field in the token payload.
            db (AsyncSession): The database session
            crud_class (Type): CRUD class to use for looking up the refresh token.

        Returns:
            str | None: The sub's ID if verification succeeds, or None if invalid.

        Raises:
            Unauthorized: If the token is invalid or expired.
        """
        # Init crud
        ref_token_crud = crud_class(db=db)

        try:
            # Decode and validate the token
            payload = jwt.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=["HS256"],
            )

            # Extract and validate the 'sub' field
            sub: str | None = payload.get("sub")
            if not sub:
                raise Unauthorized("Invalid Token")

            # Ensure the token is of type 'access'
            if payload.get("type") != "access":
                raise Unauthorized("Token type is invalid")

            # Validate the 'sub' structure
            sub_parts = sub.split("-")
            if sub_parts[0] != sub_head or len(sub_parts) < 2:
                raise Unauthorized("Invalid Token")

            # Check: valid ref id
            ref_token = await ref_token_crud.get(id=int(payload["ref_id"]))
            if not ref_token or not bool(ref_token.is_active):
                raise Unauthorized("Invalid Refresh Token")

            # Check: ref token isnt expired
            ref_expired_at: datetime = ref_token.created_at + timedelta(
                hours=self.refresh_expire_in
            )
            if datetime.now() > ref_expired_at.replace(tzinfo=None):
                raise Unauthorized("Invalid Token")

            # Return the ID part of 'sub'
            return sub_parts[1]

        except jwt.ExpiredSignatureError:
            raise Unauthorized("Access Token has expired")

        except jwt.PyJWTError:
            raise Unauthorized("Invalid Token")
