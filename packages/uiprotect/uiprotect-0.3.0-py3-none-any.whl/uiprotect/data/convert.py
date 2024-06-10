"""UniFi Protect Data Conversion."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from uiprotect.data.devices import (
    Bridge,
    Camera,
    Chime,
    Doorlock,
    Light,
    Sensor,
    Viewer,
)
from uiprotect.data.nvr import NVR, Event, Liveview
from uiprotect.data.types import ModelType
from uiprotect.data.user import CloudAccount, Group, User, UserLocation
from uiprotect.exceptions import DataDecodeError

if TYPE_CHECKING:
    from uiprotect.api import ProtectApiClient
    from uiprotect.data.base import ProtectModel


MODEL_TO_CLASS: dict[str, type[ProtectModel]] = {
    ModelType.EVENT: Event,
    ModelType.GROUP: Group,
    ModelType.USER_LOCATION: UserLocation,
    ModelType.CLOUD_IDENTITY: CloudAccount,
    ModelType.USER: User,
    ModelType.NVR: NVR,
    ModelType.LIGHT: Light,
    ModelType.CAMERA: Camera,
    ModelType.LIVEVIEW: Liveview,
    ModelType.VIEWPORT: Viewer,
    ModelType.BRIDGE: Bridge,
    ModelType.SENSOR: Sensor,
    ModelType.DOORLOCK: Doorlock,
    ModelType.CHIME: Chime,
}


def get_klass_from_dict(data: dict[str, Any]) -> type[ProtectModel]:
    """
    Helper method to read the `modelKey` from a UFP JSON dict and get the correct Python class for conversion.
    Will raise `DataDecodeError` if the `modelKey` is for an unknown object.
    """
    if "modelKey" not in data:
        raise DataDecodeError("No modelKey")

    model = ModelType(data["modelKey"])

    klass = MODEL_TO_CLASS.get(model)

    if klass is None:
        raise DataDecodeError("Unknown modelKey")

    return klass


def create_from_unifi_dict(
    data: dict[str, Any],
    api: ProtectApiClient | None = None,
    klass: type[ProtectModel] | None = None,
) -> ProtectModel:
    """
    Helper method to read the `modelKey` from a UFP JSON dict and convert to currect Python class.
    Will raise `DataDecodeError` if the `modelKey` is for an unknown object.
    """
    if "modelKey" not in data:
        raise DataDecodeError("No modelKey")

    if klass is None:
        klass = get_klass_from_dict(data)

    return klass.from_unifi_dict(**data, api=api)
