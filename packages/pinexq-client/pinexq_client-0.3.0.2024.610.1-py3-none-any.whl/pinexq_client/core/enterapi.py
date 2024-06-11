from typing import TypeVar, Type

import httpx

from pinexq_client.core import Entity
from pinexq_client.core.hco.hco_base import Hco

THco = TypeVar('THco', bound=Hco)


def enter_api(client: httpx.Client, entrypoint_hco_type: Type[THco], entrypoint_entity_type: Type[Entity] = Entity,
              entrypoint: str = "api/EntryPoint") -> THco:
    entry_point_response = client.get(url=entrypoint)
    entry_point_response.raise_for_status()
    entrypoint_entity = entrypoint_entity_type.model_validate_json(entry_point_response.read())

    return entrypoint_hco_type.from_entity(entrypoint_entity, client)
