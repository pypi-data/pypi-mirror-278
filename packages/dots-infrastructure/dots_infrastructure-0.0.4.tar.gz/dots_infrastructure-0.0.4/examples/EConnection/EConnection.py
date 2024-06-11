# -*- coding: utf-8 -*-
from datetime import datetime
import random
import helics as h
import logging
from dots_infrastructure import HelperFunctions
from dots_infrastructure.DataClasses import EsdlId, HelicsCalculationInformation, PublicationDescription, SubscriptionDescription
from dots_infrastructure.HelicsFederateHelpers import HelicsSimulationExecutor, HelicsValueFederateExecutor
from dots_infrastructure.Logger import LOGGER

class CalculationServiceEConnectionDispatch(HelicsValueFederateExecutor):

    def __init__(self):

        subscriptions_values = [
            SubscriptionDescription("PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        publication_values = [
            PublicationDescription(True, "EConnection", "EConnectionDispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        e_connection_period_in_seconds = 60

        calculation_information = HelicsCalculationInformation(e_connection_period_in_seconds, False, False, True, h.HelicsLogLevel.DEBUG, "EConnectionDispatch", subscriptions_values, publication_values, self.e_connection_dispatch)
        super().__init__(calculation_information)

    def e_connection_dispatch(self, param_dict : dict, simulation_time : datetime, esdl_id : EsdlId):
        pv_dispatch = HelperFunctions.get_vector_param_with_name(param_dict, "PV_Dispatch")
        ret_val = {}
        LOGGER.info(f"Executing e_connection_dispatch with pv dispatch value {pv_dispatch}")
        ret_val["EConnectionDispatch"] = pv_dispatch[0] * random.randint(1,3)
        self.influx_connector.set_time_step_data_point(esdl_id, "EConnectionDispatch", simulation_time, ret_val["EConnectionDispatch"])
        return ret_val


if __name__ == "__main__":

    helics_simulation_executor = HelicsSimulationExecutor()
    helics_simulation_executor.add_calculation(CalculationServiceEConnectionDispatch())
    helics_simulation_executor.start_simulation()