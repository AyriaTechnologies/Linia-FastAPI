from typing import Generic, Type, TypeVar, List, Optional, Dict
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Define a generic type for models
ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    """
    Base class for generic CRUD operations. This class is responsible for initializing
    the model and database session. It supports create, read, update, and delete operations.
    """

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, *, data: Dict) -> ModelType:
        """
        Create a new object in the database.
        """
        db_obj = self.model(**data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def get(self, **kwargs) -> Optional[ModelType]:
        """
        Retrieve a single object by its unique attributes.
        """
        obj = await self.db.execute(select(self.model).filter_by(**kwargs))
        return obj.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all objects with optional pagination.
        """
        statement = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(statement)
        return result.scalars().all()

    async def update(
        self, *, obj_id: uuid.UUID, update_data: Dict
    ) -> Optional[ModelType]:
        """Update an object in the database."""
        db_obj = await self.get_by_id(obj_id=obj_id)
        if db_obj:
            for key, value in update_data.items():
                setattr(db_obj, key, value)
            self.db.add(db_obj)
            await self.db.commit()
            await self.db.refresh(db_obj)
            return db_obj
        return None

    async def delete(self, *, obj_id: uuid.UUID) -> bool:
        """Delete an object from the database."""
        db_obj = await self.get_by_id(obj_id=obj_id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True
        return False

    async def get_by_id(self, obj_id: uuid.UUID) -> Optional[ModelType]:
        """
        Get a single object by its ID.
        """
        statement = select(self.model).where(self.model.id == obj_id)
        result = await self.db.execute(statement)
        return result.scalars().first()


# Helper CRUD Functions for Flexibility and Reusability


async def create_object(
    *, session: AsyncSession, model: Type[ModelType], create_data: dict
) -> ModelType:
    """
    Generic function to create an object.
    """
    db_obj = model(**create_data)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_object_by_id(
    *, session: AsyncSession, model: Type[ModelType], obj_id: uuid.UUID
) -> Optional[ModelType]:
    """
    Generic function to get an object by its ID.
    """
    statement = select(model).where(model.id == obj_id)
    result = await session.execute(statement)
    return result.scalars().first()


async def get_objects(
    *, session: AsyncSession, model: Type[ModelType], skip: int = 0, limit: int = 100
) -> List[ModelType]:
    """
    Generic function to get multiple objects with pagination.
    """
    statement = select(model).offset(skip).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()


async def update_object(
    *,
    session: AsyncSession,
    model: Type[ModelType],
    obj_id: uuid.UUID,
    update_data: dict,
) -> Optional[ModelType]:
    """
    Generic function to update an object.
    """
    db_obj = await get_object_by_id(session=session, model=model, obj_id=obj_id)
    if db_obj:
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    return None


async def delete_object(
    *, session: AsyncSession, model: Type[ModelType], obj_id: uuid.UUID
) -> bool:
    """
    Generic function to delete an object.
    """
    db_obj = await get_object_by_id(session=session, model=model, obj_id=obj_id)
    if db_obj:
        await session.delete(db_obj)
        await session.commit()
        return True
    return False
