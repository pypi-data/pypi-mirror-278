from pydantic import BaseModel
from typing import Any, Optional, Dict


class Story(BaseModel):
    name: str
    meta: Optional[Dict[str, Any]]
    parent: str
    full_path: str
    kwargs: Optional[Dict[str, Any]]
    docs: Optional[str]
    source: Optional[str]
    typehints: Optional[Dict[str, str]]
