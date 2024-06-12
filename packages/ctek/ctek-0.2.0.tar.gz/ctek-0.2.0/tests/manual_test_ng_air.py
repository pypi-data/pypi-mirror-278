import pytest

from ctek import NanogridAir


@pytest.mark.asyncio
async def test_nanogrid_air_print_ip():
    ip = await NanogridAir().get_ip()
    print(f"Retrieved IP: {ip}")


@pytest.mark.asyncio
async def test_nanogrid_air_print_status():
    status = await NanogridAir().fetch_status()
    print(f"Status: {status.device_info.mac}")


@pytest.mark.asyncio
async def test_nanogrid_air_print_meter_data():
    meter_data = await NanogridAir().fetch_meter_data()
    print(f"Meter data: {meter_data}")


@pytest.mark.asyncio
async def test_nanogrid_air_print_meterraw():
    meterraw = await NanogridAir().fetch_meterraw()
    print(f"Meter raw: {meterraw}")


@pytest.mark.asyncio
async def test_nanogrid_air_print_evse():
    evse = await NanogridAir().fetch_evse()
    print(f"EVSE data: {evse}")


@pytest.mark.asyncio
async def test_invalid_ip():
    with pytest.raises(ConnectionError):
        evse = await NanogridAir(device_ip="1.2.3.4").fetch_evse()
        print(f"EVSE data: {evse}")
