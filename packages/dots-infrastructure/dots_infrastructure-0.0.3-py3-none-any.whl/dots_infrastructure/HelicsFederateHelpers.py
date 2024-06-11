from concurrent.futures import ThreadPoolExecutor
from typing import List
import helics as h
import helics as h
from esdl import esdl, EnergySystem

from dots_infrastructure.DataClasses import CalculationServiceInput, CalculationServiceOutput, HelicsCalculationInformation, HelicsFederateInformation, HelicsMessageFederateInformation, SimulatorConfiguration
from dots_infrastructure.EsdlHelper import get_connected_input_esdl_objects, get_energy_system_from_base64_encoded_esdl_string
from dots_infrastructure.Logger import LOGGER
from dots_infrastructure.HelperFunctions import generate_publications_from_value_descriptions, get_simulator_configuration_from_environment


class HelicsFederateExecutor:

    def __init__(self, simulator_configuration : SimulatorConfiguration):
        self.simulator_configuration = simulator_configuration

    def destroy_federate(self, fed):
        # Adding extra time request to clear out any pending messages to avoid
        #   annoying errors in the broker log. Any message are tacitly disregarded.
        h.helicsFederateRequestTime(fed, h.HELICS_TIME_MAXTIME)
        h.helicsFederateDisconnect(fed)
        h.helicsFederateDestroy(fed)
        LOGGER.info("Federate finalized")

    def init_federate_info(self, info : HelicsFederateInformation):
        federate_info = h.helicsCreateFederateInfo()
        h.helicsFederateInfoSetBroker(federate_info, self.simulator_configuration.broker_ip)
        h.helicsFederateInfoSetBrokerPort(federate_info, self.simulator_configuration.broker_port)
        h.helicsFederateInfoSetTimeProperty(federate_info, h.HelicsProperty.TIME_PERIOD, info.time_period_in_seconds)
        h.helicsFederateInfoSetFlagOption(federate_info, h.HelicsFederateFlag.UNINTERRUPTIBLE, info.uninterruptible)
        h.helicsFederateInfoSetFlagOption(federate_info, h.HelicsFederateFlag.WAIT_FOR_CURRENT_TIME_UPDATE, info.wait_for_current_time_update)
        h.helicsFederateInfoSetFlagOption(federate_info, h.HelicsFlag.TERMINATE_ON_ERROR, info.terminate_on_error)
        h.helicsFederateInfoSetCoreType(federate_info, h.HelicsCoreType.ZMQ)
        h.helicsFederateInfoSetIntegerProperty(federate_info, h.HelicsProperty.INT_LOG_LEVEL, info.log_level)
        return federate_info

class HelicsEsdlMessageFederateExecutor(HelicsFederateExecutor):
    def __init__(self, simulator_configuration : SimulatorConfiguration, info : HelicsMessageFederateInformation):
        super().__init__(simulator_configuration)
        self.helics_message_federate_information = info

    def init_federate(self):
        federate_info = self.init_federate_info(self.helics_message_federate_information)
        self.message_federate = h.helicsCreateMessageFederate(f"{self.simulator_configuration.model_id}", federate_info)
        self.message_enpoint = h.helicsFederateRegisterEndpoint(self.message_federate, self.helics_message_federate_information.endpoint_name)

    def wait_for_esdl_file(self) -> esdl.EnergySystem:
        self.message_federate.enter_executing_mode()
        h.helicsFederateRequestTime(self.message_federate, h.HELICS_TIME_MAXTIME)
        esdl_file_base64 = h.helicsMessageGetString(h.helicsEndpointGetMessage(self.message_enpoint))
        self.destroy_federate(self.message_federate)
        
        return get_energy_system_from_base64_encoded_esdl_string(esdl_file_base64)

class HelicsValueFederateExecutor(HelicsFederateExecutor):

    def __init__(self, simulator_configuration : SimulatorConfiguration, info : HelicsCalculationInformation):
        super().__init__(simulator_configuration)
        self.input_dict : dict[str, List[CalculationServiceInput]] = {}
        self.output_dict : dict[str, List[CalculationServiceOutput]] = {}
        self.helics_value_federate_info = info

    def init_outputs(self, info : HelicsCalculationInformation, value_federate : h.HelicsValueFederate):
        outputs = generate_publications_from_value_descriptions(info.outputs, self.simulator_configuration)
        for output in outputs:
            key = f'{output.esdl_asset_type}/{output.output_name}/{output.output_esdl_id}'
            if output.global_flag:
                pub = h.helicsFederateRegisterGlobalPublication(value_federate, key, output.output_type, output.output_unit)
            else:
                pub = h.helicsFederateRegisterPublication(value_federate, key, output.output_type, output.output_unit)
            output.helics_publication = pub
            if output.output_esdl_id in self.output_dict:
                self.output_dict[output.output_esdl_id].append(output)
            else:
                self.output_dict[output.output_esdl_id] = [output]

    def init_inputs(self, info : HelicsCalculationInformation, energy_system : esdl.EnergySystem, value_federate : h.HelicsValueFederate):
        inputs : List[CalculationServiceInput] = []
        for esdl_id in self.simulator_configuration.esdl_ids:
            inputs_for_esdl_object = get_connected_input_esdl_objects(esdl_id, self.simulator_configuration.calculation_services, info.inputs, energy_system)
            inputs.extend(inputs_for_esdl_object)

        for input in inputs:
            sub_key = f'{input.esdl_asset_type}/{input.input_name}/{input.input_esdl_id}'
            LOGGER.info(f"Adding Subscription {sub_key} for esdl id: {input.simulator_esdl_id} ")
            sub = h.helicsFederateRegisterSubscription(value_federate, sub_key, input.input_unit)
            input.helics_input = sub

            if input.input_esdl_id in self.input_dict:
                self.input_dict[input.simulator_esdl_id].append(input)
            else:
                self.input_dict[input.simulator_esdl_id] = [input]

    def init_federate(self, energy_system : EnergySystem):
        federate_info = self.init_federate_info(self.helics_value_federate_info)
        value_federate = h.helicsCreateValueFederate(f"{self.simulator_configuration.model_id}/{self.helics_value_federate_info.calculation_name}", federate_info)

        self.init_inputs(self.helics_value_federate_info, energy_system, value_federate)
        self.init_outputs(self.helics_value_federate_info, energy_system, value_federate)
        self.calculation_function = self.helics_value_federate_info.calculation_function
        self.value_federate = value_federate

    def get_helics_value(self, helics_sub : CalculationServiceInput):
        LOGGER.debug(f"Getting value for subscription: {helics_sub.input_name} with type: {helics_sub.input_type}")
        input_type = helics_sub.input_type
        sub = helics_sub.helics_input
        if input_type == h.HelicsDataType.BOOLEAN:
            return h.helicsInputGetBoolean(sub)
        elif input_type == h.HelicsDataType.COMPLEX_VECTOR:
            return h.helicsInputGetComplexVector(sub)
        elif input_type == h.HelicsDataType.DOUBLE:
            return h.helicsInputGetDouble(sub)
        elif input_type == h.HelicsDataType.COMPLEX:
            return h.helicsInputGetComplex(sub)
        elif input_type == h.HelicsDataType.INT:
            return h.helicsInputGetInteger(sub)
        elif input_type == h.HelicsDataType.JSON:
            return h.helicsInputGetString(sub)
        elif input_type == h.HelicsDataType.NAMED_POINT:
            return h.helicsInputGetNamedPoint(sub)
        elif input_type == h.HelicsDataType.STRING:
            return h.helicsInputGetString(sub)
        elif input_type == h.HelicsDataType.RAW:
            return h.helicsInputGetRawValue(sub)
        elif input_type == h.HelicsDataType.TIME:
            return h.helicsInputGetTime(sub)
        elif input_type == h.HelicsDataType.VECTOR:
            return h.helicsInputGetVector(sub)
        elif input_type == h.HelicsDataType.ANY:
            return h.helicsInputGetBytes(sub)
        else:
            raise ValueError("Unsupported Helics Data Type")

    def publish_helics_value(self, helics_output : CalculationServiceOutput, value):
        LOGGER.debug(f"Publishing value: {value} for publication: {helics_output.output_name} with type: {helics_output.output_type}")
        pub = helics_output.helics_publication
        output_type = helics_output.output_type
        if output_type == h.HelicsDataType.BOOLEAN:
            h.helicsPublicationPublishBoolean(pub, value)
        elif output_type == h.HelicsDataType.COMPLEX_VECTOR:
            h.helicsPublicationPublishComplexVector(pub, value)
        elif output_type == h.HelicsDataType.DOUBLE:
            h.helicsPublicationPublishDouble(pub, value)
        elif output_type == h.HelicsDataType.COMPLEX:            
            h.helicsPublicationPublishComplex(pub, value)
        elif output_type == h.HelicsDataType.INT:
            h.helicsPublicationPublishInteger(pub, value)
        elif output_type == h.HelicsDataType.JSON:
            h.helicsPublicationPublishString(pub, value)
        elif output_type == h.HelicsDataType.NAMED_POINT:
            h.helicsPublicationPublishNamedPoint(pub, value)
        elif output_type == h.HelicsDataType.STRING:
            h.helicsPublicationPublishString(pub, value)
        elif output_type == h.HelicsDataType.RAW:
            h.helicsPublicationPublishRaw(pub, value)
        elif output_type == h.HelicsDataType.TIME:
            h.helicsPublicationPublishTime(pub, value)
        elif output_type == h.HelicsDataType.VECTOR:
            h.helicsPublicationPublishVector(pub, value)
        elif output_type == h.HelicsDataType.ANY:
            h.helicsPublicationPublishBytes(pub, value)
        else:
            raise ValueError("Unsupported Helics Data Type")

    def start_value_federate(self):
        h.helicsFederateEnterExecutingMode(self.value_federate)
    
        LOGGER.info("Entered HELICS execution mode")
    
        hours = 24 * 7 # replace by simulation parameters
        total_interval = int(60 * 60 * hours) # replace by simulation parameters
        update_interval = int(h.helicsFederateGetTimeProperty(self.value_federate, h.HELICS_PROPERTY_TIME_PERIOD))
        grantedtime = 0
    
        # As long as granted time is in the time range to be simulated...
        while grantedtime < total_interval:
            requested_time = grantedtime + update_interval
            grantedtime = h.helicsFederateRequestTime(self.value_federate, requested_time)

            for esdl_id in self.simulator_configuration.esdl_ids:
                calculation_params = {}
                if esdl_id in self.input_dict:
                    inputs = self.input_dict[esdl_id]
                    for helics_input in inputs:
                        calculation_params[helics_input.input_name] = self.get_helics_value(helics_input)
                LOGGER.info(f"Executing calculation for esdl_id {esdl_id} at time {grantedtime}")
                pub_values = self.calculation_function(calculation_params)

                outputs = self.output_dict[esdl_id]
                for output in outputs:
                    value_to_publish = pub_values[output.output_name]
                    self.publish_helics_value(output, value_to_publish)

        self.destroy_federate(self.value_federate)

class HelicsSimulationExecutor:

    def __init__(self):
        self.simulator_configuration = get_simulator_configuration_from_environment()
        self.calculations: List[HelicsCalculationInformation] = []
        self.energy_system = None

    def add_calculation(self, info : HelicsCalculationInformation):
        self.calculations.append(info)

    def init_simulation(self) -> esdl.EnergySystem:
        esdl_message_federate = HelicsEsdlMessageFederateExecutor(self.simulator_configuration, HelicsMessageFederateInformation(60, False, False, True, h.HelicsLogLevel.DEBUG, 'esdl'))
        esdl_message_federate.init_federate()
        energy_system = esdl_message_federate.wait_for_esdl_file()

        return energy_system

    def start_simulation(self):
        self.energy_system = self.init_simulation()
        executor = ThreadPoolExecutor(max_workers=len(self.calculations))
        for calculation in self.calculations:
            federate_executor = HelicsValueFederateExecutor(self.simulator_configuration, calculation)
            federate_executor.init_federate(self.energy_system)
            executor.submit(federate_executor.start_value_federate)