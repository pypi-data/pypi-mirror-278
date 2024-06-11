import random
import helics as h
import logging

from dots_infrastructure.DataClasses import HelicsCalculationInformation, PublicationDescription
from dots_infrastructure.HelicsFederateHelpers import HelicsSimulationExecutor

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def battery_calculation(param_dict : dict):
    ret_val = {}
    ret_val["EV_current"] = 0.25 * random.randint(1,3)
    return ret_val


if __name__ == "__main__":

    publictations_values = [
        PublicationDescription(True, "PVInstallation", "EV_current", "A", h.HelicsDataType.DOUBLE)
    ]

    subscriptions_values = []
    calculation_information = HelicsCalculationInformation(30, False, False, True, h.HelicsLogLevel.DEBUG, "battery_calculation", subscriptions_values, publictations_values, battery_calculation)
    helics_simulation_executor = HelicsSimulationExecutor()
    helics_simulation_executor.add_calculation(calculation_information)
    helics_simulation_executor.start_simulation()