from base64 import b64decode
from typing import List
from esdl.esdl_handler import EnergySystemHandler

from esdl import esdl
from esdl import EnergySystem
from dots_infrastructure.DataClasses import CalculationServiceInput, EsdlId, SubscriptionDescription

def get_energy_system_from_base64_encoded_esdl_string(esdl_string_base64) -> EnergySystem:
    esdl_string = b64decode(esdl_string_base64 + b"==".decode("utf-8")).decode("utf-8")
    esh = EnergySystemHandler()
    esh.load_from_string(esdl_string)
    return esh.get_energy_system()

def get_model_esdl_object(esdl_id: EsdlId, energy_system: EnergySystem) -> esdl:
    if energy_system.id == esdl_id:
        return energy_system
    # Iterate over all contents of the EnergySystem
    for obj in energy_system.eAllContents():
        if hasattr(obj, "id") and obj.id == esdl_id:
            return obj
    raise IOError(f"ESDL_ID '{esdl_id}' not found in provided ESDL file")

def extract_calculation_service_name(calculation_services: List[str], esdl_obj) -> str:
    esdl_obj_type_name = type(esdl_obj).__name__
    name = next(
        (
            calc_service_name
            for calc_service_name in calculation_services
            if calc_service_name == esdl_obj_type_name
        ),
        None,
    )
    
    return name

def add_connected_esdl_object(subscriptions: List[SubscriptionDescription], calculation_services: List[str], input_descriptions : List[SubscriptionDescription], connected_asset: esdl, simulator_asset: esdl.EnergyAsset):
    calc_service_name = extract_calculation_service_name(calculation_services, connected_asset)

    if calc_service_name:
        input_description = next((input_description for input_description in input_descriptions if input_description.esdl_type == calc_service_name), None)
        if input_description:
            subscriptions.append(CalculationServiceInput(input_description.esdl_type, input_description.input_name, connected_asset.id, input_description.input_unit, input_description.input_type, simulator_asset.id))


def add_calc_services_from_ports(
    calculation_services: List[str],
    connected_input_esdl_objects: List[SubscriptionDescription],
    input_descriptions : List[SubscriptionDescription],
    model_esdl_asset: esdl.EnergyAsset,
):
    for port in model_esdl_asset.port:
        if isinstance(port, esdl.InPort):
            for connected_port in port.connectedTo:
                connected_asset = connected_port.eContainer()
                add_connected_esdl_object(
                    connected_input_esdl_objects, calculation_services, input_descriptions, connected_asset, model_esdl_asset
                )

def add_calc_services_from_non_connected_objects(
    calculation_services: List[str],
    connected_input_esdl_objects: List[SubscriptionDescription],
    input_descriptions : List[SubscriptionDescription],
    energy_system: EnergySystem,
    model_esdl_asset: esdl.EnergyAsset
):
    for esdl_obj in energy_system.eAllContents():
        if not isinstance(esdl_obj, esdl.EnergyAsset) and hasattr(esdl_obj, "id"):
            add_connected_esdl_object(
                connected_input_esdl_objects, calculation_services, input_descriptions, esdl_obj, model_esdl_asset
            )
    add_connected_esdl_object(connected_input_esdl_objects, calculation_services, input_descriptions, energy_system, model_esdl_asset)

def add_calc_services_from_all_objects(
    calculation_services: List[str],
    connected_input_esdl_objects: List[SubscriptionDescription],
    input_descriptions : List[SubscriptionDescription],
    energy_system: EnergySystem,    
    model_esdl_asset: esdl.EnergyAsset
):
    for esdl_obj in energy_system.eAllContents():
        if hasattr(esdl_obj, "id"):
            add_connected_esdl_object(
                connected_input_esdl_objects, calculation_services, input_descriptions, esdl_obj, model_esdl_asset
            )

def get_connected_input_esdl_objects(
    esdl_id: EsdlId,
    calculation_services: List[str],
    input_descriptions : List[SubscriptionDescription],
    energy_system: EnergySystem,
) -> List[CalculationServiceInput]:
    model_esdl_obj = get_model_esdl_object(esdl_id, energy_system)

    connected_input_esdl_objects: List[CalculationServiceInput] = []
    if isinstance(model_esdl_obj, esdl.EnergyAsset):
        add_calc_services_from_ports(
            calculation_services, connected_input_esdl_objects, input_descriptions, model_esdl_obj
        )
        add_calc_services_from_non_connected_objects(
            calculation_services, connected_input_esdl_objects, input_descriptions, energy_system, model_esdl_obj
        )
    else:
        add_calc_services_from_all_objects(
            calculation_services, connected_input_esdl_objects, input_descriptions, energy_system, model_esdl_obj
        )
    return connected_input_esdl_objects