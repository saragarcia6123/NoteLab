import re

valid_name_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
valid_path_pattern = re.compile(r'^[a-zA-Z0-9](?:[a-zA-Z0-9 ._-]*[a-zA-Z0-9])?\.[a-zA-Z0-9_-]+$')

def to_snake_case(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def verify_name(name: str) -> bool:
    return valid_name_pattern.match(name) is not None
