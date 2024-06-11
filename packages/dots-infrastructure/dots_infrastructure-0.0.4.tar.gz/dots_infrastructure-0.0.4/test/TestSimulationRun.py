import base64
from datetime import datetime
import random
import unittest
import helics as h
import multiprocessing

from unittest.mock import MagicMock
from dots_infrastructure import HelperFunctions
from threading import Thread

from dots_infrastructure.DataClasses import EsdlId, HelicsCalculationInformation, PublicationDescription, SimulatorConfiguration, SubscriptionDescription
from dots_infrastructure.EsdlHelper import get_energy_system_from_base64_encoded_esdl_string
from dots_infrastructure.HelicsFederateHelpers import HelicsSimulationExecutor, HelicsValueFederateExecutor
from dots_infrastructure.Logger import LOGGER
from infra.InfluxDBMock import InfluxDBMock

BROKER_TEST_PORT = 23404
START_DATE_TIME = datetime(2024, 1, 1, 0, 0, 0)
SIMULATION_DURATION_IN_SECONDS = 900

with open("C:\\Users\\20180029\\repos\\dots-infrastructure\\test\\test.esdl", mode="r") as esdl_file:
    encoded_base64_esdl = base64.b64encode(esdl_file.read().encode('utf-8')).decode('utf-8')

HelicsSimulationExecutor.init_simulation = MagicMock(return_value=encoded_base64_esdl)

MS_TO_BROKER_DISCONNECT = 60000

def start_helics_broker():
    broker = h.helicsCreateBroker("zmq", "helics_broker_test", "-f 2 --loglevel=debug --timeout='60s'")
    broker.wait_for_disconnect(MS_TO_BROKER_DISCONNECT)

def simulator_environment_e_pv():
        return SimulatorConfiguration("PVInstallation", ['176af591-6d9d-4751-bb0f-fac7e99b1c3d','b8766109-5328-416f-9991-e81a5cada8a6'], "Mock-PV", "127.0.0.1", BROKER_TEST_PORT, "test-id", SIMULATION_DURATION_IN_SECONDS, START_DATE_TIME, "test-host", "test-port", "test-username", "test-password", "test-database-name", ["PVInstallation", "EConnection"])

class CalculationServicePVDispatch(HelicsValueFederateExecutor):

    def __init__(self, output_file_name, period_in_seconds):
        HelperFunctions.get_simulator_configuration_from_environment = simulator_environment_e_pv
        publictations_values = [
            PublicationDescription(True, "PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE)
        ]
        subscriptions_values = []
        info = HelicsCalculationInformation(period_in_seconds, False, False, True, h.HelicsLogLevel.DEBUG, "pvdispatch_calculation", subscriptions_values, publictations_values, self.pvdispatch_calculation)
        super().__init__(info)
        self.influx_connector = InfluxDBMock(output_file_name)

    def pvdispatch_calculation(self, param_dict : dict, simulation_time : datetime, esdl_id : EsdlId):
        ret_val = {}
        LOGGER.info(f"Executing pvdispatch_calculation")
        ret_val["PV_Dispatch"] = 0.25 * random.randint(1,20)
        self.influx_connector.set_time_step_data_point(esdl_id, "PV_Dispatch", simulation_time, ret_val["PV_Dispatch"])
        return ret_val

def simulator_environment_e_connection():
        return SimulatorConfiguration("EConnection", ["f006d594-0743-4de5-a589-a6c2350898da"], "Mock-Econnection", "127.0.0.1", BROKER_TEST_PORT, "test-id", SIMULATION_DURATION_IN_SECONDS, START_DATE_TIME, "test-host", "test-port", "test-username", "test-password", "test-database-name", ["PVInstallation", "EConnection"])

class CalculationServiceEConnectionDispatch(HelicsValueFederateExecutor):

    def __init__(self, output_file_name, period_in_seconds):
        HelperFunctions.get_simulator_configuration_from_environment = simulator_environment_e_connection

        subscriptions_values = [
            SubscriptionDescription("PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        publication_values = [
            PublicationDescription(True, "EConnection", "EConnectionDispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        calculation_information = HelicsCalculationInformation(period_in_seconds, False, False, True, h.HelicsLogLevel.DEBUG, "EConnectionDispatch", subscriptions_values, publication_values, self.e_connection_dispatch)
        super().__init__(calculation_information)
        self.influx_connector = InfluxDBMock(output_file_name)

    def e_connection_dispatch(self, param_dict : dict, simulation_time : datetime, esdl_id : EsdlId):
        pv_dispatch = HelperFunctions.get_vector_param_with_name(param_dict, "PV_Dispatch")
        ret_val = {}
        LOGGER.info(f"Executing e_connection_dispatch with pv dispatch value {pv_dispatch}")
        ret_val["EConnectionDispatch"] = pv_dispatch[0] * random.randint(1,3)
        self.influx_connector.set_time_step_data_point(esdl_id, "EConnectionDispatch", simulation_time, ret_val["EConnectionDispatch"])
        return ret_val

class TestSimulation(unittest.TestCase):

    def test_simulation_run_starts_correctly(self):
        # Arrange 
        broker_process = multiprocessing.Process(target = start_helics_broker)
        broker_process.start()

        simulation_executor = HelicsSimulationExecutor()

        e_connection_output_file = "e_connection_out.txt"
        pv_installation_output_file = "pv_installation_out.txt"
        e_connection_period = 60
        pv_period = 30
        simulation_executor.add_calculation(CalculationServiceEConnectionDispatch(e_connection_output_file, e_connection_period))
        simulation_executor.add_calculation(CalculationServicePVDispatch(pv_installation_output_file, pv_period))

        # Execute
        simulation_executor.start_simulation()
        broker_process.join()

        # Assert
        with open(e_connection_output_file, 'r') as f:
            lines = f.readlines()
        self.assertEqual(len(lines), SIMULATION_DURATION_IN_SECONDS / e_connection_period)

        with open(pv_installation_output_file, 'r') as f:
            lines = f.readlines()
        self.assertEqual(len(lines), SIMULATION_DURATION_IN_SECONDS / pv_period * 2)


if __name__ == '__main__':
    unittest.main()