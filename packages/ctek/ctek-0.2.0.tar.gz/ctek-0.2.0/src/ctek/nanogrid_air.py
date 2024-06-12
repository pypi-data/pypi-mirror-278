import logging
import socket
from dataclasses import asdict, dataclass, field
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class BaseDataClass:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def __str__(self) -> str:
        return f"{self.to_dict()}"


@dataclass
class DeviceInfo(BaseDataClass):
    serial: str
    firmware: str
    mac: str


@dataclass
class ChargeboxInfo(BaseDataClass):
    identity: str
    serial: str
    firmware: str
    endpoint: str
    port: int
    state: str
    pinned: bool


@dataclass
class MeterInfo(BaseDataClass):
    vendor: str
    type: str
    id: str


@dataclass
class OTAInfo(BaseDataClass):
    status: int
    version: str
    progress: int


@dataclass
class DeviceStatus(BaseDataClass):
    device_info: DeviceInfo
    chargebox_info: ChargeboxInfo
    meter_info: MeterInfo
    ota_info: OTAInfo


@dataclass
class MeterData(BaseDataClass):
    active_power_in: float
    active_power_out: float
    current: list[float]
    voltage: list[float]
    total_energy_active_import: int
    total_energy_active_export: int


@dataclass
class MeterRawData(BaseDataClass):
    result: str
    cpu_time_ms: int
    length: int
    data: str


@dataclass
class EVSEInfo(BaseDataClass):
    id: int
    state: int
    current: list[float]


@dataclass
class EVSEData(BaseDataClass):
    cb_id: str
    connection_status: str
    evse: list[EVSEInfo] = field(default_factory=list)


@dataclass
class NanogridAir:
    device_ip: str | None = None
    _initialized: bool = False
    _default_hostname: str = "ctek-ng-air.local"

    async def get_ip(self, hostname: str = _default_hostname) -> str | None:
        try:
            ip = socket.gethostbyname(hostname)
            logger.debug(f"Resolved hostname '{hostname}' to IP: {ip}")
            return ip
        except socket.gaierror as e:
            raise ConnectionError(
                "Could not resolve hostname '" + hostname + "'"
            ) from e

    async def initialize(self, hostname: str = _default_hostname) -> None:
        if not self._initialized:
            if not self.device_ip:
                self.device_ip = await self.get_ip(hostname)
            self._initialized = True

    def __post_init__(self) -> None:
        if self.device_ip is not None:
            self._initialized = True

    def is_initialized(self) -> bool:
        return self._initialized

    async def _fetch_data(self, endpoint: str) -> dict[str, Any]:
        await self.initialize()
        url = f"http://{self.device_ip}/{endpoint}/"
        try:
            async with aiohttp.ClientSession() as session, session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                logger.debug(f"Received data from {url}: {data}")
                if isinstance(data, list):
                    return {str(idx): item for idx, item in enumerate(data)}
                elif isinstance(data, dict):
                    return data
                else:
                    raise ValueError("Unexpected data type received")
        except aiohttp.ClientConnectionError as e:
            raise ConnectionError(f"Could not connect to {url}") from e

    async def fetch_status(self) -> DeviceStatus:
        data: dict[str, Any] = await self._fetch_data("status")

        # Get device info fields with default values if they are missing
        device_info_data = data.get("deviceInfo", {})
        device_info = DeviceInfo(
            serial=device_info_data.get("serial", ""),
            firmware=device_info_data.get("firmware", ""),
            mac=device_info_data.get("mac", ""),
        )

        # Get chargebox info fields with default values if they are missing
        chargebox_info_data = data.get("chargeboxInfo", {})
        chargebox_info = ChargeboxInfo(
            identity=chargebox_info_data.get("identity", ""),
            serial=chargebox_info_data.get("serial", ""),
            firmware=chargebox_info_data.get("firmware", ""),
            endpoint=chargebox_info_data.get("endpoint", ""),
            port=chargebox_info_data.get("port", 0),
            state=chargebox_info_data.get("state", ""),
            pinned=chargebox_info_data.get("pinned", False),
        )

        # Get meter info fields with default values if they are missing
        meter_info_data = data.get("meterInfo", {})
        meter_info = MeterInfo(
            vendor=meter_info_data.get("vendor", ""),
            type=meter_info_data.get("type", ""),
            id=meter_info_data.get("id", ""),
        )

        # Get OTA info fields with default values if they are missing
        ota_info_data = data.get("otaInfo", {})
        ota_info = OTAInfo(
            status=ota_info_data.get("status", 0),
            version=ota_info_data.get("version", ""),
            progress=ota_info_data.get("progress", 0),
        )

        return DeviceStatus(
            device_info=device_info,
            chargebox_info=chargebox_info,
            meter_info=meter_info,
            ota_info=ota_info,
        )

    async def fetch_meter_data(self) -> MeterData:
        data: dict[str, Any] = await self._fetch_data("meter")
        return MeterData(
            active_power_in=data["activePowerIn"],
            active_power_out=data["activePowerOut"],
            current=data["current"],
            voltage=data["voltage"],
            total_energy_active_import=data["totalEnergyActiveImport"],
            total_energy_active_export=data["totalEnergyActiveExport"],
        )

    async def fetch_meterraw(self) -> list[MeterRawData]:
        data = await self._fetch_data("meterraw")
        return [
            MeterRawData(
                result=item["result"],
                cpu_time_ms=item["cpu_time_ms"],
                length=item["len"],
                data=item["data"],
            )
            for item in list(data.values())
        ]

    async def fetch_evse(self) -> list[EVSEData]:
        data = await self._fetch_data("evse")
        return [
            EVSEData(
                cb_id=item["cb_id"],
                connection_status=item["connection_status"],
                evse=[
                    EVSEInfo(
                        id=evse_item["id"],
                        state=evse_item["state"],
                        current=evse_item["current"],
                    )
                    for evse_item in item["evse"]
                ],
            )
            for item in list(data.values())
        ]
