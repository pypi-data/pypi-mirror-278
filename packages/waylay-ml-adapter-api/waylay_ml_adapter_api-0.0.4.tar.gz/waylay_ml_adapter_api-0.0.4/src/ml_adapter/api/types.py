"""Types related to model loading."""

import io
from pathlib import Path
from typing import Generic, Protocol, TypeVar

from .data.common import Parameters

AssetLocation = Path
AssetSource = AssetLocation | str | io.IOBase


def as_location(location: AssetLocation | str | None) -> AssetLocation:
    """Parse a location specification as location path."""
    return Path(location or ".")


#: Model Instance Type Variable
MI = TypeVar("MI")
#: Native Model Inference Request
MREQ = TypeVar("MREQ")
#: Native Model Inference Response
MRES = TypeVar("MRES")
#: Marshalled Model Inference Request
RREQ = TypeVar("RREQ")
#: Marshalled Model Inference Response
RRES = TypeVar("RRES")

#: Native Model Scalar or Tensor representation
V = TypeVar("V")
#: Dicts of Scalar or Tensor
VDict = dict[str, V]
#: Scalar or Tensor or Dicts of it.
VorDict = V | VDict


class AsyncModelInvoker(Protocol, Generic[MREQ, MRES]):
    """Protocol for model invocation."""

    async def __call__(self, req: MREQ, *args: MREQ, **kwargs) -> MRES:
        """Signature for model invocation."""


class AsyncModelInvokerWithParams(Protocol, Generic[MREQ, MRES]):
    """Protocol for a model invocation with output parameters."""

    async def __call__(
        self, req: MREQ, *args: MREQ, **kwargs
    ) -> tuple[MRES, Parameters]:
        """Signature for a model invocation with output parameters."""


class SyncModelInvoker(Protocol, Generic[MREQ, MRES]):
    """Protocol for model invocation."""

    def __call__(self, req: MREQ, *args: MREQ, **kwargs) -> MRES:
        """Signature for model invocation."""


class SyncModelInvokerWithParams(Protocol, Generic[MREQ, MRES]):
    """Protocol for a model invocation with output parameters."""

    def __call__(self, req: MREQ, *args: MREQ, **kwargs) -> tuple[MRES, Parameters]:
        """Signature for a model invocation with output parameters."""


class AsyncSerializableModel(Protocol, Generic[MI]):
    """Protocol for a model that provides its own serialization."""

    async def save(self: MI, location: AssetLocation, **kwargs):
        """Signature for save the model instance."""

    @classmethod
    async def load(cls: type[MI], location: AssetLocation, **kwargs) -> MI:
        """Signature to load the model instance."""


class SyncSerializableModel(Protocol, Generic[MI]):
    """Protocol for a model that provides its own serialization."""

    def save(self: MI, location: AssetLocation, **kwargs):
        """Signature for save the model instance."""

    @classmethod
    def load(cls: type[MI], location: AssetLocation, **kwargs) -> MI:
        """Signature to load the model instance."""


SerializableModel = AsyncSerializableModel | SyncSerializableModel

ModelInvoker = (
    AsyncModelInvoker[MREQ, MRES]
    | AsyncModelInvokerWithParams[MREQ, MRES]
    | SyncModelInvoker[MREQ, MRES]
    | SyncModelInvokerWithParams[MREQ, MRES]
)
