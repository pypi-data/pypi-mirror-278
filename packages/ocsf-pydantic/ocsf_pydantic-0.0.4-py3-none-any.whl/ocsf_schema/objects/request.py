from pydantic import BaseModel
from .container import Container

class RequestElements(BaseModel):
    """
    The Request Elements object describes characteristics of an API request.
    """

    uid: str  # The unique request identifier.

    # Optional:
    containers: list[Container] | None = None
    data: dict | None = None # The additional data that is associated with the api request.
    flags: list[str] | None = None
