from pydantic import BaseModel, Field, RootModel, ValidationError, validator
from typing import Any, Dict, List, Optional, Set, TypeVar, Generic, Type, Callable, Literal, Union
from ..connector import BaseExecutionOutput
import yaml
import importlib
import functools
import inspect
from types import NoneType


class EventDefinition(BaseModel):
    event: str
    description: str


class FunctionParams(BaseModel):
    name: str
    require: bool
    description: str
    type: str

class FunctionReturn(BaseModel):
    name: str
    description: str
    type: str

class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: List[FunctionParams]
    returns: Union[str, FunctionReturn]

class ActionsDefinition(BaseModel):
    triggers: Optional[List[EventDefinition]]
    functions: Optional[List[FunctionDefinition]]

class CredentialDefinition(BaseModel):
    handler: str
    required: bool = False

class BlockConfigDefinition(BaseModel):
    apiVersion: str = Field(..., alias='apiVersion')
    type: str
    metadata: Dict[str, Any]
    handler: str
    modes: List[str]
    credentials: Optional[Dict[str, CredentialDefinition]] = {}
    actions: ActionsDefinition
    pool: Optional[Literal['cpu-short', 'cpu-long', 'cpu-nointerrupt', 'gpu']] = 'cpu-short'
    timeout: Optional[int] = 90
                 
def read_block_definition(yaml_path: str) -> BlockConfigDefinition:
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return BlockConfigDefinition(**data)

def register_trigger_handler(event_name: str) -> Callable:
    """Register a given function as a handler for a event trigger named `event_name`."""
    def decorator(func: Callable[..., BaseExecutionOutput]) -> Callable[..., BaseExecutionOutput]:
        # Use functools.wraps to preserve the metadata of the original function
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> BaseExecutionOutput:
            # Call the original function
            result = func(*args, **kwargs)
            # Check if the return type of the function is as expected
            if result == None:
                return result
            if not isinstance(result, BaseExecutionOutput):
                raise TypeError(f"Expected return type {BaseExecutionOutput.__name__}, got {type(result).__name__}")
            result.mode = "trigger"
            result.event = event_name
            return result
        # Mark the function with the event name
        wrapper._event_name = event_name
        return wrapper
    return decorator

def register_function(function_name: str) -> Callable:
    def decorator(func: Callable[..., BaseExecutionOutput]) -> Callable[..., BaseExecutionOutput]:
        """Register a given function as a handler for a YAML function named `function_name`."""
        # Use functools.wraps to preserve the metadata of the original function
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> BaseExecutionOutput:
            # Call the original function
            result = func(*args, **kwargs)
            # Check if the return type of the function is as expected
            if result == None:
                return result
            if not isinstance(result, BaseExecutionOutput):
                raise TypeError(f"Expected return type {BaseExecutionOutput.__name__}, got {type(result).__name__}")
            result.mode = "function"
            result.event = function_name
            return result
        # Mark the function with the event name
        wrapper._function_name = function_name
        return wrapper
    return decorator

class HandlerType(type):
    def __new__(cls, name, bases, namespace):
        cls_instance = super().__new__(cls, name, bases, namespace)
        cls_instance.trigger_handlers = {}
        cls_instance.functions = {}
        # Register marked methods as handlers
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and hasattr(attr_value, '_event_name'):
                event_name = getattr(attr_value, '_event_name')
                cls_instance.trigger_handlers[event_name] = attr_value
            if callable(attr_value) and hasattr(attr_value, '_function_name'):
                output_name = getattr(attr_value, '_function_name')
                cls_instance.functions[output_name] = attr_value
        return cls_instance
    
class DefaultPipelineBlock(metaclass=HandlerType):
    trigger_handlers: Dict[str, Callable]
    functions: Dict[str, Callable]
    def __init__(self, config, instance_config, credentials, memory=None):
        super().__init__()
        self.config = config
        self.instance_config = instance_config
        self.credentials=credentials
        self.memory = memory

        config_dict = config.dict()
        self.instance_config = self.validate_instance_config(self.instance_config).model_dump()
        if 'triggers' in config_dict['actions']:
            assert hasattr(self, 'trigger_handlers'), "No trigger handlers are defined"
            for trigger in config_dict['actions']['triggers']:
                if trigger['event'] not in self.trigger_handlers:
                    raise ValueError(f"Trigger event {trigger['event']} defined in manifest, but no handler is defined!")
        if 'functions' in config_dict['actions']:
            assert hasattr(self, 'functions'), "No functions are defined"
            for output in config_dict['actions']['functions']:
                if output['name'] not in self.functions:
                    raise ValueError(f"Function {output['name']} defined in manifest, but no handler is defined!")
                sig = inspect.signature(self.functions[output['name']])
                params = {
                    param.name: param.annotation.__name__ for param in sig.parameters.values() if param.name != "self"
                }
                if len(params) != len(output['parameters']):
                    raise ValueError(f"Function {output['name']} specification defines {len(output['parameters'])} parameters but code defines {len(params)} parameters!")
                for item in output['parameters']:
                    name = item['name']
                    if name not in params.keys():
                        raise ValueError(f"Function {output['name']} parameter '{name}' not defined!")
                    if item['type'] != params[name]:
                        raise ValueError(f"Function {output['name']} parameter '{name}' types do not match specification '{params[name]}'!")
                    

                    
    def validate_instance_config(self, parameters: dict) -> BaseModel:
        """Code to validate the instance configuration. This function must raise an error if the configuration is invalid."""
        raise NotImplementedError("You must implement an instance configuration validator!")

class StatefulPipelineBlock(DefaultPipelineBlock):
    def __init__(self, config, instance_config):
        super().__init__(config=config, instance_config=instance_config)
    def listener_start(self):
        raise NotImplementedError("You must implement a listener start function!")
    def listener_stop(self):
        raise NotImplementedError("You must implement a listener stop function!")
    
def load_block(full_class_string):
    """
    Dynamically imports a class from a given string, handling nested modules.

    :param full_class_string: 'package.module.ClassName'
    :return: class object
    """
    module_name, class_name = full_class_string.rsplit('.', 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls