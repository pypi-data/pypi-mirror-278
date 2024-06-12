import logging
import uuid

import fastapi

from neos_common.authorization import base, signer
from neos_common.base import Action, ResourceLike
from neos_common.client.hub_client import HubClient

logger = logging.getLogger(__name__)


class AccessValidator(base.AccessValidator):
    def __init__(self, hub_client: HubClient) -> None:
        self._hub_client = hub_client

    async def validate(
        self,
        user_id: uuid.UUID,
        actions: list[Action],
        resources: list[ResourceLike],
        logic_operator: str,
        *,
        return_allowed_resources: bool = False,
    ) -> tuple[uuid.UUID, list[str]]:
        return await self._hub_client.validate_token(
            principal=user_id,
            actions=actions,
            resources=[resource.urn for resource in resources],
            logic_operator=logic_operator,
            return_allowed_resources=return_allowed_resources,
        )


class SignatureValidator(base.SignatureValidator):
    def __init__(self, hub_client: HubClient) -> None:
        self._hub_client = hub_client

    async def validate(
        self,
        request: fastapi.Request,
        actions: list[Action],
        resources: list[ResourceLike],
        logic_operator: str,
        *,
        return_allowed_resources: bool = False,
    ) -> tuple[uuid.UUID, list[str]]:
        validator = signer.Validator()

        payload = await request.body()

        auth_type, access_key_id, scope, challenge, signature = validator.challenge_v4(
            request.method,
            request.url,
            request.headers,
            payload,
        )

        return await self._hub_client.validate_signature(
            access_key_id,
            auth_type.split("-")[0],
            scope,
            challenge,
            signature,
            actions,
            [resource.urn for resource in resources],
            logic_operator=logic_operator,
            return_allowed_resources=return_allowed_resources,
        )
