from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.crud import CRUDBase
from app.User import models


class UserCRUD(CRUDBase[models.User]):
    def __init__(self, db: AsyncSession):
        super().__init__(models.User, db)


class UserRefreshTokenCRUD(CRUDBase[models.UserRefreshToken]):
    def __init__(self, db: AsyncSession):
        super().__init__(models.UserRefreshToken, db)

    async def delete_tokens(self, user: models.User):
        """
        Delete all user tokens
        """

        # Delete tokens
        await self.db.execute(delete(self.model).filter_by(user_id=user.id))
        await self.db.commit()

        return True
