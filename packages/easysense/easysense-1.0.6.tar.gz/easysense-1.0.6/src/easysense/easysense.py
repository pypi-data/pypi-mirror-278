import importlib
import logging
import subprocess
import sys
from typing import Dict, Any


log = logging.getLogger(__name__)


class Easysense:
    sensors: Dict[str, Any] = {}

    def give_data(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method!")

    @staticmethod
    def install_dependency(*dependencies: str):
        # Styling
        lib_sgpl = "library" if len(dependencies) == 1 else "libraries"
        libv_sgpl = "library is" if len(dependencies) == 1 else "libraries are"

        print(f"This sensor requires the following {lib_sgpl} to be installed: {', '.join(dependencies)}")
        install = ask_install(
            prompt="Do you want to install them now? (Y/n) ",
            error_msg="Input must be 'Y' or 'n'."
        )
        if install:
            for dependency in dependencies:
                try:
                    importlib.import_module(dependency)
                except ImportError:
                    failed_dependencies = []
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
                        subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
                    except Exception as e:
                        log.error(f"Error occured during automatic import for '{dependency}': {e}")
                        failed_dependencies.append(dependency)

                    if failed_dependencies:
                        print(f"Couln't install the following {lib_sgpl} automatically. Please install it manually: '{failed_dependencies}'")
                        exit(0)
        else:
            raise ImportError(f"The following {libv_sgpl} required for this sensor: {', '.join(dependencies)}")


def ask_install(prompt: str, error_msg: str = "Please enter valid data."):
    user_input = input(prompt)
    try:
        if user_input.strip().lower() in "yn":
            return user_input.lower() == "y"
        else:
            raise ValueError

    except ValueError:
        print(error_msg)
        return ask_install(prompt, error_msg)
