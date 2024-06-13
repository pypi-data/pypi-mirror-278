from enum import Enum
from pydantic import BaseModel

from .reputation import Reputation

class ObservableTypeId(Enum):
    """
    The observable value type identifier.
    """
    Unknown: int = 0 # Unknown observable data type.
    Other: int = 99 # The observable data type is not mapped. See the `type` attribute,
                    # which may contain data source specific value.

class Observable(BaseModel):
    """
    The observable object is a pivot element that contains related information found
    in many places in the event.
    """

    name: str # The full name of the observable attribute. The `name` is a
              # pointer/reference to an attribute within the event data. For example:
              # `file.name`.
    type_id: ObservableTypeId # The observable value type identifier.


    # Optional:
    reputation: Reputation | None = None
    type: str | None = None # The observable value type name.
    value: str | None = None # The value associated with the observable attribute. The meaning of the
                             # value depends on the observable type.<br/>If the `name`
                             # refers to a scalar attribute, then the `value` is the value
                             # of the attribute.<br/>If the `name` refers to an object
                             # attribute, then the `value` is not populated.
