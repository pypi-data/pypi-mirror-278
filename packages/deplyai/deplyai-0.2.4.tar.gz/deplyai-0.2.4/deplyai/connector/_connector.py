from pydantic import BaseModel, Field, RootModel, ValidationError, validator
from typing import Any, Dict, Optional
from google.protobuf import json_format

class BaseExecutionOutput(BaseModel):
    walltime: float | None = None # populated by stage runnner
    stdout: str | None = None # populated by stage runnner
    stderr: str | None = None # populated by stage runnner
    statusCode: int # 0 = SUCCESS. provided by user, or overidden by stage runner if exception thrown
    mode: str | None = None # injected by registration handlers
    event: str | None = None # injected by registration handlers
    output: str = None # actual output

def serialize_output(output: BaseExecutionOutput):
    raise NotImplementedError()