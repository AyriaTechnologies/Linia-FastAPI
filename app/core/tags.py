from functools import lru_cache
from pydantic import BaseModel


class RouteTags(BaseModel):
    """
    Base model for app route tags
    """

    # User Module
    USER: str = "User Endpoints"


@lru_cache
def get_tags():
    """
    Returns the app RouteTags
    """
    return RouteTags()
