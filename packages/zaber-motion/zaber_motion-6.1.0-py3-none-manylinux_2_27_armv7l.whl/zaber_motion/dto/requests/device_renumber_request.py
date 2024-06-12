# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass
from typing import Any, Dict
import decimal
import zaber_bson


@dataclass
class DeviceRenumberRequest:

    interface_id: int = 0

    first_address: int = 0

    @staticmethod
    def zero_values() -> 'DeviceRenumberRequest':
        return DeviceRenumberRequest(
            interface_id=0,
            first_address=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceRenumberRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceRenumberRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': int(self.interface_id),
            'firstAddress': int(self.first_address),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceRenumberRequest':
        return DeviceRenumberRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            first_address=data.get('firstAddress'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.interface_id is None:
            raise ValueError(f'Property "InterfaceId" of "DeviceRenumberRequest" is None.')

        if not isinstance(self.interface_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "InterfaceId" of "DeviceRenumberRequest" is not a number.')

        if int(self.interface_id) != self.interface_id:
            raise ValueError(f'Property "InterfaceId" of "DeviceRenumberRequest" is not integer value.')

        if self.first_address is None:
            raise ValueError(f'Property "FirstAddress" of "DeviceRenumberRequest" is None.')

        if not isinstance(self.first_address, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "FirstAddress" of "DeviceRenumberRequest" is not a number.')

        if int(self.first_address) != self.first_address:
            raise ValueError(f'Property "FirstAddress" of "DeviceRenumberRequest" is not integer value.')
