from app.User import models


async def format_user(user: models.User):
    """
    Format user obj to dict
    """
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_active": user.is_active,
        "updated_at": user.updated_at,
        "created_at": user.created_at,
    }
