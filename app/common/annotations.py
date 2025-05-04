from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session

DatabaseSession = Annotated[AsyncSession, Depends(get_session)]
