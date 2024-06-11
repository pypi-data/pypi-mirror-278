from datetime import datetime
import random
import helics as h

from dots_infrastructure import HelperFunctions
from dots_infrastructure.DataClasses import EsdlId, HelicsCalculationInformation, PublicationDescription
from dots_infrastructure.HelicsFederateHelpers import HelicsSimulationExecutor, HelicsValueFederateExecutor
from dots_infrastructure.Logger import LOGGER

class CalculationServicePVDispatch(HelicsValueFederateExecutor):

    def __init__(self):
        publictations_values = [
            PublicationDescription(True, "PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE)
        ]
        subscriptions_values = []

        pv_installation_period_in_seconds = 30
        info = HelicsCalculationInformation(pv_installation_period_in_seconds, False, False, True, h.HelicsLogLevel.DEBUG, "pvdispatch_calculation", subscriptions_values, publictations_values, self.pvdispatch_calculation)
        super().__init__( info)

    def pvdispatch_calculation(self, param_dict : dict, simulation_time : datetime, esdl_id : EsdlId):
        ret_val = {}
        LOGGER.info(f"Executing pvdispatch_calculation")
        ret_val["PV_Dispatch"] = 0.25 * random.randint(1,20)
        self.influx_connector.set_time_step_data_point(esdl_id, "PV_Dispatch", simulation_time, ret_val["PV_Dispatch"])
        return ret_val

if __name__ == "__main__":
    helics_simulation_executor = HelicsSimulationExecutor()
    helics_simulation_executor.add_calculation(CalculationServicePVDispatch())
    helics_simulation_executor.start_simulation()