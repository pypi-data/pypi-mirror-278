import asyncio
import importlib.util
import inspect
import logging
import os
import sys
import time
import warnings
from typing import Optional, List

import yaml
from wiresense import Wiresense

from easysense import Easysense


# Constants
PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
SENSOR_FOLDER = f"{PATH}/sensors"
CONFIG_FILE = f"{PATH}/config.yaml"

# Logging config
date = time.strftime("%d-%m-%Y")
log_file_path = f"{PATH}/logs/log_{date}.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    handlers=[
        logging.FileHandler(filename=log_file_path, mode="a")
    ]
)

log = logging.getLogger(__name__)


def load_config(config_section: str = None):
    if not os.path.exists(CONFIG_FILE):
        warn_msg = "config.yaml is missing! -> You will always be prompted to select required parameter"
        log.warning(warn_msg)
        warnings.warn(warn_msg)
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f) or {}
    if config_section:
        section = config.get(config_section, {})
    else:
        section = config

    if not section:
        log.warning("Some values are missing in config.yaml -> Check the github repo to see whats missing")
    return section


def _load_sensors():
    for filename in os.listdir(SENSOR_FOLDER):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_name = os.path.splitext(filename)[0].removesuffix("_sensor")
            module_path = os.path.normpath(os.path.join(SENSOR_FOLDER, filename))

            if module_name in Easysense.sensors:
                log.warning(f"Sensor with name '{module_name}' already exists. -> Skipping this one")
                warnings.warn(f"Sensor with name '{module_name}' already exists.")
                return

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)

            try:
                spec.loader.exec_module(module)
                Easysense.sensors[module_name] = module
                log.info(f"Sensor '{module_name}' loaded!")
            except ImportError as ie:
                print("")
            except Exception as e:
                warn_msg = f"Sensor '{module_name}' not loaded!\nExtension raised an error: {e}"
                log.warning(warn_msg)
                warnings.warn(warn_msg)
    log.info(f"Loaded {len(Easysense.sensors)} sensors.")


def list_sensors():
    print("Available sensors:")
    sorted_sensors = sorted(Easysense.sensors.keys())
    for i, s in enumerate(sorted_sensors, 1):
        print(f"{i}. {s}")


def ask_valid_input(prompt: str, d_type: type, *, x_range: Optional[List[float]] = None, error_msg: str = "Please enter valid data."):
    user_input = input(prompt)
    try:
        value = d_type(user_input)
        if d_type in [int, float] and x_range:
            if not x_range[0] <= value <= x_range[1]:
                raise ValueError
        elif d_type is bool:
            if user_input.strip().lower() in "yn":
                return user_input.lower() == "y"
            else:
                raise ValueError
        return value

    except ValueError:
        print(error_msg)
        return ask_valid_input(prompt, d_type, x_range=x_range, error_msg=error_msg)


def select_sensor(settings) -> (str, Easysense):
    s_sensor = settings.get("selected_sensor", "")

    if s_sensor:
        matching_sensor = Easysense.sensors.get(s_sensor)
        if matching_sensor:
            print(f"Auto-selected Sensor from config.yaml: {s_sensor}")
            log.info(f"Auto-selected Sensor from config.yaml: {s_sensor}")
            return s_sensor
        else:
            print(f"Sensor with name '{s_sensor}' not found")
            log.info("Sensor selected in config.yaml not found -> Prompting user to select sensor manually")

    list_sensors()
    print()

    numb = ask_valid_input(
        prompt="Enter the number of the sensor you want to use: ",
        d_type=int,
        x_range=[1, len(Easysense.sensors)],
        error_msg="This number is not in the list."
    )

    s_name = sorted(Easysense.sensors.keys())[numb - 1]
    print(f"Selected Sensor: {s_name}")
    log.info(f"Selected Sensor: {s_name}")

    return s_name


def select_interval(settings) -> float:
    s_interval = settings.get("read_interval", -1)
    x_range = [0, float("inf")]

    if x_range[0] < s_interval < x_range[1]:
        selected_interval = s_interval
        print(f"Auto-selected Interval from config.yaml: {selected_interval}")
        log.info(f"Auto-selected Interval from config.yaml: {selected_interval}")
        return selected_interval
    elif s_interval != -1:
        print(f"Invalid read_interval in config.yaml")
        log.warning(f"Invalid read_interval in config.yaml -> Prompting user to enter interval manually")

    selected_interval = ask_valid_input(
        prompt="Enter the interval at which the data of the selected sensor should be read (in seconds): ",
        d_type=float,
        x_range=x_range,
        error_msg="Interval must be a float >= 0"
    )
    print(f"Selected Interval: {selected_interval}")
    log.info(f"Selected Interval: {selected_interval}")
    return selected_interval


def select_print_data(settings) -> bool:
    s_print_data = settings.get("print_data_in_cmd")

    if s_print_data is None:
        selected_print_data = ask_valid_input(
            prompt="Should the data be printed here too? (Y/n): ",
            d_type=bool,
            error_msg="Input must be 'Y' or 'n'."
        )
        print(f"Selected Print cmd: {selected_print_data}")
        log.info(f"Selected Print cmd: {selected_print_data}")
    else:
        selected_print_data = s_print_data
        print(f"Auto-selected Print data from config.yaml: {selected_print_data}")
        log.info(f"Auto-selected Print data from config.yaml: {selected_print_data}")

    return selected_print_data


def use_sensor(s_name: str):
    if s_name in Easysense.sensors:
        sensor = Easysense.sensors.get(s_name)

        for name, obj in inspect.getmembers(sensor, inspect.isclass):
            if issubclass(obj, Easysense) and obj is not Easysense:
                sensor_class = obj
                sensor_instance = sensor_class()
                return sensor_instance
        else:
            log.error(f"No subclass inheriting from Easysense found in sensor '{s_name}'")
            raise RuntimeError(f"No subclass inheriting from Easysense found in sensor '{s_name}'")
    else:
        log.error(f"Selected Sensor '{s_name}' not found!")
        raise RuntimeError(f"Selected Sensor '{s_name}' not found!")


async def setup_wiresense(s_name, interval, csv_file_path, print_data):
    log.info("Configuring Wiresense...")
    await Wiresense.config({
        "port": 8080
    })

    sensor = use_sensor(s_name)
    selected_sensor = Wiresense(s_name, sensor.give_data, csv_file_path)

    log.info("Wiresense Configured")
    try:
        print("Now Running, press CTRL + C to exit.")
        log.info("Running sensor.execute() in an infinite loop...")
        if print_data:
            while True:
                payload = await selected_sensor.execute()
                values = [f"{key}: {value}" for key, value in payload.get("data").items()]
                print(", ".join(values))
                await asyncio.sleep(interval)
        else:
            while True:
                await selected_sensor.execute()
                await asyncio.sleep(interval)
    except KeyboardInterrupt:
        log.info("Exited App: KeyboardInterrupt")
        exit(0)


def display():
    print("╔═════════════════════════════╗")
    print("║          Easysense          ║")
    print("║      -----------------      ║")
    print("║         Pre-written         ║")
    print("║    sensor implementations   ║")
    print("║        for Wiresense        ║")
    print("╚═════════════════════════════╝")
    print("https://github.com/Saladrian/easysense.py")
    print()


def main():
    _load_sensors()

    display()
    config_settings = load_config("settings")

    if not Easysense.sensors:
        print("No Sensors found!")
        log.error("No Sensors found!")
        sys.exit(1)

    s_name = select_sensor(config_settings)
    sel_interval = select_interval(config_settings)
    print_data = select_print_data(config_settings)

    folder_path = config_settings.get("csv_folder_path", "")
    if not folder_path:
        folder_path = "./data"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{s_name}.csv")

    asyncio.run(setup_wiresense(s_name, sel_interval, file_path, print_data))


if __name__ == '__main__':
    main()
