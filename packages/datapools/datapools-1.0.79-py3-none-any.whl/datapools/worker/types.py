from typing import NamedTuple, Optional

# from ..common.storage import FileStorage
from ..common.types import DatapoolContentType
from pydantic import AnyUrl
from ..common.session_manager import Session


class WorkerContext(NamedTuple):
    session: Session
    # storage: FileStorage


class WorkerTask(NamedTuple):
    url: AnyUrl
    content_type: Optional[DatapoolContentType] = None
