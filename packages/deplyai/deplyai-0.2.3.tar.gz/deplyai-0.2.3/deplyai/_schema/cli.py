from pydantic import BaseModel, Field, RootModel, ValidationError, field_validator
from typing import Any, Dict, List, Optional, Set

class ProfileCredentials(BaseModel):
    tenant: int
    token: str
    id_token: str