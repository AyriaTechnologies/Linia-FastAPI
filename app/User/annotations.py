from typing import Annotated

from fastapi import Depends

from app.User import models, selectors

CurrentUser = Annotated[models.User, Depends(selectors.get_current_user)]
