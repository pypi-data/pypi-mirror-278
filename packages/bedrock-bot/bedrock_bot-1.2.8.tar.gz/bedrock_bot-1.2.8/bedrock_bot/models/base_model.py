from __future__ import annotations

import json
import logging
from enum import Enum

import boto3
from botocore.config import Config
from rich.console import Console

logger = logging.getLogger()

console = Console()


class ConversationRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"

    def __str__(self) -> str:
        return self.value


class _BedrockModel:
    """Base class for all models.

    Usage:
    Add a message to the conversation and invoke the model with `model.invoke(message)`.

    Creating new implementations of this base model:
    - Define extra params to inject to the invoke call on self.model_params
    - Provide a model_id to `super().__init__()`
    - If your model needs a different body than the default, overwrite `self._create_invoke_body()`
    """

    name = "Base Model"
    model_params = {}  # noqa: RUF012
    _model_id: str

    def __init__(
        self,
        boto_config: None | Config = None,
    ) -> None:
        if not boto_config:
            boto_config = Config()
        self._bedrock = boto3.client("bedrock-runtime", config=boto_config)
        self.messages = []

    def reset(self) -> None:
        self.messages = []

    def append_message(self, role: ConversationRole, message: str) -> None:
        self.messages.append({"role": role.value, "content": message})

    def invoke(self, message: str) -> str:
        self.append_message(ConversationRole.USER, message)

        response = self._invoke()
        self.append_message(ConversationRole.ASSISTANT, response)
        return response

    def _create_invoke_body(self) -> dict:
        raise NotImplementedError

    def _handle_response(self, body: dict) -> str:
        raise NotImplementedError

    def _invoke(self) -> str:
        body = self._create_invoke_body() | self.model_params

        with console.status("[bold green]Waiting for response..."):
            logger.info(f"Sending current messages to AI: {self.messages}")
            response = self._bedrock.invoke_model(
                modelId=self._model_id,
                body=json.dumps(body),
            )
            body = json.loads(response["body"].read())

            return self._handle_response(body)
