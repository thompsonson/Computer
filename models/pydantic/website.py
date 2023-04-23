from pydantic import BaseModel
from typing import List, Optional


class FileData(BaseModel):
    identifier: str
    url: str
    description: Optional[str]


class WebsiteData(BaseModel):
    html_content: str
    images: List[FileData]
    files: List[FileData]
