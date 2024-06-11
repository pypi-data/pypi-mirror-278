import asyncio

from bleak import AdvertisementData, BleakClient, BleakScanner, BLEDevice

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from rich import print  # noqa
from tc66c2mqtt.cli_app import cli


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def scan(verbosity: int):
    """
    Discover Bluetooth devices and there services/descriptors
    """
    setup_logging(verbosity=verbosity)

    async def device_info(device: BLEDevice):
        print(f'Connect to {device}...', flush=True, end='')

        async with BleakClient(device) as client:
            print('connected.')

            for service in client.services:
                print('_' * 79)
                print('Service:', service)

                for char in service.characteristics:
                    print(f'{char.properties=}')
                    if 'read' in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                        except Exception as err:
                            print('\tERROR:', err)
                        else:
                            print(f'\tread: {value=}')

                    for descriptor in char.descriptors:
                        print('Descriptor:', descriptor)
                        try:
                            value = await client.read_gatt_descriptor(descriptor.handle)
                        except Exception as err:
                            print(f'\tError: {err}')
                        else:
                            print(f'\t{value=}')

                print()

    async def main():
        async with BleakScanner() as scanner:
            seen_addresses = set()
            print('Scanning...\n')

            async for device, advertisement_data in scanner.advertisement_data():
                device: BLEDevice
                advertisement_data: AdvertisementData

                if device.address in seen_addresses:
                    return
                seen_addresses.add(device.address)

                print('New device found:', device)
                print()
                print(advertisement_data)
                print()
                await device_info(device)

    asyncio.run(main())
