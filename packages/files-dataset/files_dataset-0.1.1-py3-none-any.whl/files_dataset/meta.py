from typing import Mapping, Literal
from pydantic import BaseModel

class Meta(BaseModel):

  class Archive(BaseModel):
    archive: str
    """Path to the archive, or a glob pattern to multiple archives"""
    format: Literal['tar', 'zip'] | None = None
    num_files: int | None = None

  files_dataset: Mapping[str, Archive]