import json
from services.models import Endpoint

def load_endpoints() -> list[Endpoint]:
    """Load endpoints from endpoints.json"""
    with open("endpoints.json") as f:
        raw = json.load(f)
    return [Endpoint(**e) for e in raw]