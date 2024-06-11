
import json
import os
from typing import List

from dots_infrastructure.DataClasses import CalculationServiceInput, CalculationServiceOutput, PublicationDescription, SimulatorConfiguration, SubscriptionDescription
from dots_infrastructure.Logger import LOGGER


def get_simulator_configuration_from_environment() -> SimulatorConfiguration:
    esdl_ids = os.getenv("esdl_ids", "e1b3dc89-cee8-4f8e-81ce-a0cb6726c17e;f006d594-0743-4de5-a589-a6c2350898da").split(";")
    connected_services_json = os.getenv("connected_services", '{"e1b3dc89-cee8-4f8e-81ce-a0cb6726c17e":[{"esdl_type":"PVInstallation","connected_services":["1830a516-fae5-4cc7-99bd-6e9a5d175a80"]}],"f006d594-0743-4de5-a589-a6c2350898da":[{"esdl_type":"PVInstallation","connected_services":["176af591-6d9d-4751-bb0f-fac7e99b1c3d","b8766109-5328-416f-9991-e81a5cada8a6"]}]}')
    connected_services = json.loads(connected_services_json)
    esdl_type = os.getenv("esdl_type", "test-type")
    model_id = os.getenv("model_id", "test-id")
    broker_ip = os.getenv("broker_ip", "127.0.0.1")
    broker_port = int(os.getenv("broker_port", "30000"))
    calculation_services = os.getenv("calculation_services")
    return SimulatorConfiguration(esdl_type, connected_services, esdl_ids, model_id, broker_ip, broker_port, calculation_services)

def generate_publications_from_value_descriptions(value_descriptions : List[PublicationDescription], simulator_configuration : SimulatorConfiguration) -> List[CalculationServiceOutput]:
    ret_val = []
    for value_description in value_descriptions:
        for esdl_id in simulator_configuration.esdl_ids:
            ret_val.append(CalculationServiceOutput(value_description.global_flag, value_description.esdl_type, value_description.input_name, esdl_id, value_description.data_type, value_description.input_unit))
    return ret_val

def get_single_param_with_name(param_dict : dict, name : str):
    for key in param_dict.keys():
        if name in key:
            return param_dict[key]

def get_vector_param_with_name(param_dict : dict, name : str):
    return [value for key, value in param_dict.items() if name in key]
