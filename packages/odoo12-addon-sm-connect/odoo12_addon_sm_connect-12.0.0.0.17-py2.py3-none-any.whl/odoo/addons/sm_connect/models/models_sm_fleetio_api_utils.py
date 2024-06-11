# -*- coding: utf-8 -*-
from odoo import _
from odoo.exceptions import UserError
import requests, json
import logging

_logger = logging.getLogger(__name__)

class sm_fleetio_api_utils(object):

    __instance = None
    __fleetio_api_token = None
    __fleetio_account_token = None

    @staticmethod
    def get_instance(parent):
        if sm_fleetio_api_utils.__instance is None:
            sm_fleetio_api_utils(parent)

        return sm_fleetio_api_utils.__instance

    @staticmethod
    def drop_instance():
        if sm_fleetio_api_utils.__instance is not None:
            sm_fleetio_api_utils.__instance = None

    def __init__(self, parent):
        if sm_fleetio_api_utils.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            sm_fleetio_api_utils.__instance = self
            company = parent.env.user.company_id
            self.__fleetio_api_token = company.sm_fleetio_api_token
            self.__fleetio_account_token = company.sm_fleetio_account_token
            self.__headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Token ' + (self.__fleetio_api_token or ""),
                'Account-Token': self.__fleetio_account_token or ""
            }
            self.__test_mode = company.sm_fleetio_test_mode

    def check_api_settings(self):
        """ This function checks if the variables set are correct for the connection. """

        if self.__fleetio_api_token and self.__fleetio_account_token:
            if len(self.__fleetio_api_token)>1 and len(self.__fleetio_account_token)>1:
                return True
        return False

    def get_id_fuel_type(self, odoo_name):

        odoo_fleetio_map = {
            "gasoline"  : "Gasoline",
            "diesel"    : "Diesel",
            "lpg"       : "LPG",
            "electric"  : "Electric",
            "hybrid"    : "Plug-in Hybrid",
        }

        name = odoo_fleetio_map.get(odoo_name)

        url = 'https://secure.fleetio.com/api/v1/fuel_types'
        response = requests.get(url, headers=self.__headers)


        if response.status_code != 200:
            _logger.error(f"\n\nFAILED API CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")
            raise UserError(_("Failed to retrieve Vehicle Fuel Type from Fleetio: \n\n%s") % response.text)

        _logger.debug(f"\nAPI CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")
        # Now we search for the ID based on the parameter name
        fuel_types = response.json()
        result_id = False
        for fuel_type in fuel_types:
            if fuel_type['name'] == name:
                result_id = fuel_type['id']
                break

        # If there are fuel types and none matched with the name
        # retireve the ID of the first entry's id
        if not result_id and len(fuel_types):
            result_id = fuel_types[0]['id']

        return result_id

    def payload_composer(self, vehicle):
        if vehicle and not vehicle._name=="fleet.vehicle":
            raise Exception("Wrong Class of vehicle, expected 'fleet.vehicle' but got: " + vehicle._name)

        """ Creates the payload for Create and Update requests based on a specific vehicle """

        name                = str(vehicle.license_plate).replace(" ", "")
        license_plate       = str(vehicle.license_plate).replace(" ", "")
        #fuel_type_id        = str(self.get_id_fuel_type(vehicle.fuel_type or "electric"))
        vehicle_type_name   = vehicle.vehicle_type.capitalize() # i.e Car or Van
        vehicle_status_name = "Verificar" if self.__test_mode else "Pendent de ubicació"
        make                = vehicle.model_id.brand_id.name.capitalize() or ""
        model               = vehicle.model_id.name + (vehicle.sm_version or "")
        year                = vehicle.acquisition_date.year if vehicle.acquisition_date else 0
        vin                 = vehicle.vin_sn
        color               = vehicle.color or ""
        fuel_tank_capacity  = vehicle.battery_size or 0
        ownership           = vehicle.ownership or ""

        # Map the fields of the records of fleet.vehicle to the data structure of Fleetio
        payload = {
            "name": name,
            "license_plate": license_plate,
            "system_of_measurement":"metric",
            "meter_unit": "km",
            "primary_meter_unit": "km",
            "vehicle_type_name": vehicle_type_name,
            #"fuel_type_id": fuel_type_id,
            "make": make,
            "model": model,
            "year": year,
            "vin": vin,
            "color" : color,
            "ownership":ownership,
            "specs" : {
                "fuel_tank_capacity": fuel_tank_capacity,
            },
            # Add the rest of the fields here
        }

        # Only set the status on creation (doesn't have external ID yet)
        if not vehicle.fleetio_id:
            payload["vehicle_status_name"] = vehicle_status_name

        return payload

    def search_vehicles(self, vehicle=None):
        if vehicle and not vehicle._name=="fleet.vehicle":
            raise Exception("Wrong Class of vehicle, expected 'fleet.vehicle' but got: " + vehicle._name)
        
        base_url = 'https://secure.fleetio.com/api/v1/vehicles'

        def create_url_payload(start_cursor=None, filters=None):
            """ This method will create the url parameters that will be appended to the base url"""
            to_url_embed =  {
                "per_page"          : 50,
                "start_cursor"      : start_cursor,

                #TODO: Add filter part it will come as an array
                #"filter"            : 
            }
            result = "?"
            for element in to_url_embed:
                if to_url_embed[element]:
                    result += str(element) + "=" + str(to_url_embed[element]) + "&"
            return result

        def get_records(response):
            """ Sets the structure of records on a dictionary indexed on license_plate """
            return {record.get("license_plate").replace(" ", ""): record for record in response.json().get("records", [])}

        payload_filters = []
        if vehicle:
            payload_filters = [
                ("license_plate", "like", vehicle.license_plate)
            ]

        url = base_url + create_url_payload()

        response = requests.get(url, headers=self.__headers) # Kick-off
        vehicles_json = get_records(response)

        while response.status_code==200 and response.json().get("next_cursor"):
            url = base_url + create_url_payload(start_cursor=response.json().get("next_cursor"))
            response = requests.get(url, headers=self.__headers)
            vehicles_json.update(get_records(response))

        if response.status_code != 200:
            _logger.error(f"\n\nFAILED API CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")
            raise UserError(_("Failed to retrieve vehicles in Fleetio: \n\n%s") % response.text)

        _logger.debug(f"\nAPI CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")

        return vehicles_json

    def create_vehicle(self, vehicle):
        url = "https://secure.fleetio.com/api/v1/vehicles"

        payload = self.payload_composer(vehicle)

        #_logger.info(self.get_vehicles())

        response = requests.post(url, headers=self.__headers, data=json.dumps(payload))

        if response.status_code != 201:
            _logger.error(f"\n\nFAILED API CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")
            raise UserError(_("Failed to create vehicle in Fleetio: \n\n%s") % response.text)

        _logger.debug(f"\nAPI CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")

        response_json = response.json()
        vehicle.fleetio_id = response_json.get("id")
        return response_json

    def update_vehicle(self, vehicle):
        url = "https://secure.fleetio.com/api/v1/vehicles/{}".format(vehicle.fleetio_id)

        payload = self.payload_composer(vehicle)

        response = requests.patch(url, headers=self.__headers, data=json.dumps(payload))

        if response.status_code != 200:
            _logger.error(f"\n\nFAILED API CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")
            raise UserError(_("Failed to update vehicle in Fleetio: \n\n%s") % response.text)
        
        _logger.debug(f"\nAPI CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")

        return response.json()

    def archive_vehicle(self, vehicle):
        url = "https://secure.fleetio.com/api/v1/vehicles/{}/archive".format(vehicle.fleetio_id)

        response = requests.patch(url, headers=self.__headers)

        _logger.info(f"\n\n\tCode: {response.status_code}\n\t\tResponse: {response.text}")

        if response.status_code != 204:
            _logger.error(f"\n\nFAILED API CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")
            raise UserError(_("Failed to archive vehicle in Fleetio: \n\n%s") % response.text)
        
        _logger.debug(f"\nAPI CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")

        vehicle.fleetio_archived = True

        return True

    def restore_vehicle(self, vehicle):
        url = "https://secure.fleetio.com/api/v1/vehicles/{}/restore".format(vehicle.fleetio_id)

        response = requests.patch(url, headers=self.__headers)

        if response.status_code != 204:
            _logger.error(f"\n\nFAILED API CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")
            raise UserError(_("Failed to restore vehicle in Fleetio: \n\n%s") % response.text)
        
        _logger.debug(f"\nAPI CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {self.__headers}")

        vehicle.fleetio_archived = False

        return True
