from enum import Enum

from .application import Application
from ocsf_schema.objects.product import Product

class ApplicationLifecycleActivityId(Enum):
    Install: int = 1
    Remove: int = 2
    Start: int = 3
    Stop: int = 4
    Restart: int = 5
    Enable: int = 6
    Disable: int = 7
    Update: int = 8

class ApplicationLifecycle(Application):
    """
    Application Lifecycle events report installation, removal, start, stop of an
    application or service.
    """

    activity_id: ApplicationLifecycleActivityId | None = None
    app: Product | None = None # The application that was affected by the lifecycle event.  This also
                               # applies to self-updating application systems.
