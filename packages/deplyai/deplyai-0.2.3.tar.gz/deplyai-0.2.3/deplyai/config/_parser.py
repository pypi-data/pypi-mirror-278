import yaml

from deplyai._schema import Pipeline
from deplyai._utils.graph import cyclic

from pydantic import ValidationError

def read_pipeline_config(yaml_path, return_graph = False):
    """Reads the Pipeline definition file at `yaml_path` and returns the Pipeline object.
    :param yaml_path: file path to the Pipeline defintion file.
    :throws pydantic_core._pydantic_core.ValidationError if schema constraints are violated.
    :throws ValueError if uniqueness constraints are violated.
    """
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return parse_pipeline_config(data, return_graph)

def parse_pipeline_config(data, return_graph = False):
    pipeline = Pipeline(**data)
    config = pipeline.model_dump()
    graph = {}
    for item in config['stages']:
        stage_name = item['id']
        has_triggers = 'triggers' in item and len(item['triggers']) > 0
        if has_triggers:
            for trg in item['triggers']:
                name = trg['name']
                if name in graph:
                    raise ValidationError(f"Trigger name  '{name}' was used more than once!")
                graph[name] = {}
        if len(item['outputs']) == 0:
            for key in graph:
                graph[key][item['id']] = []
        else:
            for out in item['outputs']:
                name = out['name']
                dest = out['destination']
                if name not in graph:
                    raise ValidationError(f"Output name '{name}' is not a valid trigger name!")
                if stage_name not in graph[name]:
                    graph[name][stage_name] = [dest]
                else:
                    graph[name][stage_name].append(dest)
    for subgraph in graph:
        if cyclic(graph[subgraph]):
            raise ValidationError(f"Graph for trigger {subgraph} is cyclic!")
    if return_graph:
        return pipeline, graph
    return pipeline