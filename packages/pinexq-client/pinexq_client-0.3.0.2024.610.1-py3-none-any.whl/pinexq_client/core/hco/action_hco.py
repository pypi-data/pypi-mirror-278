from typing import TypeVar, Self

import httpx
from httpx import Response
from httpx import URL

from pinexq_client.core import SirenException, Entity, Action, ProblemDetails, execute_action
from pinexq_client.core.hco.hco_base import ClientContainer

TEntity = TypeVar('TEntity', bound=Entity)
THcoEntity = TypeVar('THcoEntity', bound=Entity)


class ActionHco(ClientContainer):
    _client: httpx.Client
    _action: Action

    @classmethod
    def from_action_optional(cls, client: httpx.Client, action: Action | None) -> Self | None:
        if action is None:
            return None

        if action.has_parameters():
            raise SirenException(f"Error while mapping action: expected action no parameters but got some")

        instance = cls(client)
        instance._action = action
        return instance

    @classmethod
    def from_entity_optional(cls, client: httpx.Client, entity: Entity, name: str) -> Self | None:
        if entity is None:
            return None

        action = entity.find_first_action_with_name(name)
        return cls.from_action_optional(client, action)

    @classmethod
    def from_action(cls, client: httpx.Client, action: Action) -> Self:
        action = cls.from_action_optional(client, action)
        if action is None:
            raise SirenException(
                f"Error while mapping mandatory action: does not exist")
        return action

    @classmethod
    def from_entity(cls, client: httpx.Client, entity: Entity, name: str) -> Self:
        result = cls.from_entity_optional(client, entity, name)
        if result is None:
            raise SirenException(
                f"Error while mapping mandatory action {name}: does not exist")
        return result

    def _execute_internal(self) -> None | URL:
        response = execute_action(self._client, self._action)

        if isinstance(response, ProblemDetails):
            raise SirenException(
                f"Error while executing action: {response}")
        if isinstance(response, Response):
            raise SirenException(
                f"Error while executing action, unexpected response: {response}")
        return response

    def __repr__(self):
        return f"<{self.__class__.__name__}: '{self._action.name}'>"




