def generate_id(tenant, pipeline_id, version, execution_uuid, stage_id) -> int:
    # Ensure inputs are within their bit limits
    tenant &= 0xFFFFFFFF         # 32 bits
    pipeline_id &= 0xFFFF        # 16 bits
    version &= 0xFFFF            # 16 bits
    execution_uuid &= 0xFFFFFFFF  # 32 bits
    stage_id &= 0xFFFFFFFF       # 32 bits

    # Shift and combine the values to fit them in 128 bits
    result: int = (tenant << 96) | (pipeline_id << 80) | (version << 64) | (execution_uuid << 32) | stage_id

    return result

def update_id(id_128bit, tenant=None, pipeline_id=None, version=None, execution_uuid=None, stage_id=None) -> int:
    # Masks for extracting each field from the existing ID
    tenant_mask = 0xFFFFFFFF << 96
    pipeline_id_mask = 0xFFFF << 80
    version_mask = 0xFFFF << 64
    execution_uuid_mask = 0xFFFFFFFF << 32
    stage_id_mask = 0xFFFFFFFF

    # Extract current values if None is passed
    current_tenant = (id_128bit & tenant_mask) >> 96
    current_pipeline_id = (id_128bit & pipeline_id_mask) >> 80
    current_version = (id_128bit & version_mask) >> 64
    current_execution_uuid = (id_128bit & execution_uuid_mask) >> 32
    current_stage_id = id_128bit & stage_id_mask

    # Update the fields if new values are provided
    tenant = current_tenant if tenant is None else tenant
    pipeline_id = current_pipeline_id if pipeline_id is None else pipeline_id
    version = current_version if version is None else version
    execution_uuid = current_execution_uuid if execution_uuid is None else execution_uuid
    stage_id = current_stage_id if stage_id is None else stage_id

    # Combine the possibly updated values back into a single 128-bit integer
    updated_id = (tenant << 96) | (pipeline_id << 80) | (version << 64) | (execution_uuid << 32) | stage_id
    return updated_id


def parse_id(id_128bit):
    # Masks for extracting each field from the ID
    tenant_mask = 0xFFFFFFFF << 96
    pipeline_id_mask = 0xFFFF << 80
    version_mask = 0xFFFF << 64
    execution_uuid_mask = 0xFFFFFFFF << 32
    stage_id_mask = 0xFFFFFFFF

    # Extract each component by applying the mask and then right-shifting to the LSB
    tenant = (id_128bit & tenant_mask) >> 96
    pipeline_id = (id_128bit & pipeline_id_mask) >> 80
    version = (id_128bit & version_mask) >> 64
    execution_uuid = (id_128bit & execution_uuid_mask) >> 32
    stage_id = id_128bit & stage_id_mask

    # Return a dictionary with the parsed values
    return {
        'tenant': tenant,
        'pipeline_id': pipeline_id,
        'version': version,
        'execution_uuid': execution_uuid,
        'stage_id': stage_id
    }

def format_id_as_uuid(id_128bit):
    hex_str = format(id_128bit, '032x')
    uuid_str = f'{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}'
    return uuid_str

def uuid_to_128bit(uuid_str):
    hex_str = uuid_str.replace('-', '')
    id_128bit = int(hex_str, 16)
    return id_128bit
