from pydantic import BaseModel
from typing import  Optional

class BaseDocument(BaseModel):
    id: Optional[str]
    is_deleted: bool = False
    # created_on: datetime.datetime.now()

