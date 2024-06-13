__author__ = "florez@ethz.ch"
__copyright__ = ""
__license__ = "LGPLv3"
__version__ = "0.7.0"

import logging
import os

from bamboost.manager import Manager
from bamboost.simulation import Simulation
from bamboost.simulation_writer import SimulationWriter
from bamboost._config import config
from bamboost.extensions import extensions


def set_log_level(level: int = 30):
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=os.environ.get("LOGLEVEL", level))


# Set default logging level to WARNING (30)
set_log_level(30)
