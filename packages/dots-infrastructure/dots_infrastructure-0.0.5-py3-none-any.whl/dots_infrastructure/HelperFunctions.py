from datetime import datetime
import os
from typing import List

from dots_infrastructure.DataClasses import CalculationServiceOutput, PublicationDescription, SimulatorConfiguration
from dots_infrastructure.Logger import LOGGER


def get_simulator_configuration_from_environment() -> SimulatorConfiguration:
    esdl_ids = os.getenv("esdl_ids", "e1b3dc89-cee8-4f8e-81ce-a0cb6726c17e;f006d594-0743-4de5-a589-a6c2350898da").split(";")
    esdl_type = os.getenv("esdl_type", "test-type")
    model_id = os.getenv("model_id", "test-id")
    broker_ip = os.getenv("broker_ip", "127.0.0.1")
    broker_port = int(os.getenv("broker_port", "30000"))
    start_time_str = str(os.getenv("start_time", "2024-06-10 09:51:13"))
    simulation_duration_in_seconds = int(os.getenv("simulation_duration_in_seconds", 86400))
    start_time_datetime = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    calculation_services = os.getenv("calculation_services")
    simulation_id = str(os.getenv("simulation_id", "test-id"))
    influx_host = os.getenv("INFLUXDB_HOST")
    influx_port = os.getenv("INFLUXDB_PORT")
    influx_username = os.getenv("INFLUXDB_USER")
    influx_password = os.getenv("INFLUXDB_PASSWORD")
    influx_database_name = os.getenv("INFLUXDB_NAME")
    return SimulatorConfiguration(esdl_type, esdl_ids, model_id, broker_ip, broker_port,simulation_id, simulation_duration_in_seconds, start_time_datetime, influx_host, influx_port, influx_username, influx_password, influx_database_name, calculation_services)

def generate_publications_from_value_descriptions(value_descriptions : List[PublicationDescription], simulator_configuration : SimulatorConfiguration) -> List[CalculationServiceOutput]:
    ret_val = []
    for value_description in value_descriptions:
        for esdl_id in simulator_configuration.esdl_ids:
            ret_val.append(CalculationServiceOutput(value_description.global_flag, value_description.esdl_type, value_description.output_name, esdl_id, value_description.data_type, value_description.output_unit))
    return ret_val

def get_single_param_with_name(param_dict : dict, name : str):
    for key in param_dict.keys():
        if name in key:
            return param_dict[key]

def get_vector_param_with_name(param_dict : dict, name : str):
    return [value for key, value in param_dict.items() if name in key]
