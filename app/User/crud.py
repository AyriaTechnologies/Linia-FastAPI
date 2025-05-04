from sqlalchemy.ext.asyncio import AsyncSession
from app.common.crud import CRUDBase
from app.User import models


class UserCRUD(CRUDBase[models.User]):
    def __init__(self, db: AsyncSession):
        super().__init__(models.User, db)


class UserRefreshTokenCRUD(CRUDBase[models.UserRefreshToken]):
    def __init__(self, db: AsyncSession):
        super().__init__(models.UserRefreshToken, db)
