import asyncio
import time

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from rich import print  # noqa

from tc66c2mqtt.cli_app import cli
from tc66c2mqtt.mqtt_handler import Tc66cMqttHandler
from tc66c2mqtt.tc66c_bluetooth import poll
from tc66c2mqtt.user_settings import UserSettings, get_user_settings


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def publish_loop(verbosity: int):
    """
    Print TC66C data to console
    """
    setup_logging(verbosity=verbosity)
    user_settings: UserSettings = get_user_settings(verbosity=verbosity)

    tc66c_mqtt_handler = Tc66cMqttHandler(user_settings=user_settings, verbosity=verbosity)

    while True:
        try:
            asyncio.run(
                poll(
                    device_name=user_settings.device_name,
                    poll_callback=tc66c_mqtt_handler,
                )
            )
        except TimeoutError:
            print('Timeout... Retrying in 1 second...')
            time.sleep(1)
        except Exception as e:
            print(f'Error: {e}', type(e))
            print('Retrying in 1 second...')
            time.sleep(1)
