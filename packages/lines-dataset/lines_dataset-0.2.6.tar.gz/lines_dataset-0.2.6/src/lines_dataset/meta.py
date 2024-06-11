from typing import Mapping, Literal
from pydantic import BaseModel

class Meta(BaseModel):

  class File(BaseModel):
    file: str
    compression: Literal['zstd'] | None = None
    num_lines: int | None = None

  lines_dataset: Mapping[str, File]