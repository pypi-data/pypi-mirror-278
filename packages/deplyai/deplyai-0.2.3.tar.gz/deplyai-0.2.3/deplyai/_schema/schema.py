from pydantic import BaseModel, Field, RootModel, ValidationError, field_validator
from typing import Any, Dict, List, Optional, Set

class TypeSpecificConfig(RootModel):
    pass

class BlockConfig(BaseModel):
    type: str
    version: str
    typeSpecificConfig: TypeSpecificConfig
    mode: Optional[str] = None

class Trigger(BaseModel):
    name: str
    event: str
    filter: str

class Output(BaseModel):
    name: str
    destination: str
    function: str
    parameters: Dict[str, str]

class Credential(BaseModel):
    type: str 
    value: str | dict

class Stage(BaseModel):
    id: str = Field(..., max_length=255)
    type: str
    blockSpec: str
    blockConfig: BlockConfig
    credentials: Optional[Dict[str, Credential]] = {}
    triggers: List[Trigger] = []
    outputs: List[Output]
    memory: Optional[Dict[str, str]] = {}

class Pipeline(BaseModel):
    apiVersion: str = Field(..., alias='apiVersion')
    type: str
    metadata: Dict[str, Any]
    stages: List[Stage]
    @field_validator('metadata')
    def metadata_must_contain_name_and_description(cls, v):
        if 'name' not in v:
            raise ValueError("The 'metadata' field must contain the 'name' field.")
        if 'description' not in v:
            raise ValueError("The 'metadata' field must contain the 'description' field.")
        return v
