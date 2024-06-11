# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
import requests
import logging
import json


_logger = logging.getLogger(__name__)


class sm_carsharing_api_utils(object):

    __instance = None
    __cs_url = None
    __apikey = None
    __admin_group = None

    @staticmethod
    def get_instance(parent):
        if sm_carsharing_api_utils.__instance is None:
            sm_carsharing_api_utils(parent)

        return sm_carsharing_api_utils.__instance

    def __init__(self, parent):
        if sm_carsharing_api_utils.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            sm_carsharing_api_utils.__instance = self
            company = parent.env.user.company_id
            sm_carsharing_api_utils.__cs_url = company.sm_carsharing_api_credentials_cs_url
            sm_carsharing_api_utils.__apikey = company.sm_carsharing_api_credentials_api_key
            sm_carsharing_api_utils.__admin_group = company.sm_carsharing_api_credentials_admin_group

    def get_endpoint_base(self, limit=""):
        return self.__cs_url + "/api/admin/v1/" + self.__admin_group + "/" + limit

    def get_headers_base(self):
        return {'Content-type': 'application/json', 'apiKey': self.__apikey}

    def get_reservations_by_group(self, from_q=False, till_q=False, group_q=False):
        if from_q and till_q and group_q:
            return requests.get(
                self.get_endpoint_base("reservations"),
                params={'from': from_q, 'till': till_q, 'group': group_q},
                headers=self.get_headers_base())
        return False

    def post_persons_send_registration_email(self, parent, person_id=False, person_lang=False, registration_api_endpoint_overwrite=False):
        if person_id and person_lang:
            if registration_api_endpoint_overwrite:
                cs_url = registration_api_endpoint_overwrite
                endpoint = registration_api_endpoint_overwrite + \
                    "/api/admin/v1/sommobilitat/persons/" + person_id + "/sendRegistrationEmail"
            else:
                cs_url = parent.env.user.company_id.sm_carsharing_api_credentials_cs_url
                endpoint = self.get_endpoint_base(
                    "persons") + "/" + person_id + "/sendRegistrationEmail"
            headers_r = self.get_headers_base()
            headers_r['Accept-Language'] = 'ca'
            headers_r['referer'] = cs_url+'/#/'
            return requests.post(endpoint, data=json.dumps({}), headers=headers_r)
        return False

    def get_persons(self, person_id=False):
        if person_id:
            return requests.get(self.get_endpoint_base("persons") + "/" + person_id, headers=self.get_headers_base())
        return False

    def post_persons(self, data=False):
        if data:
            url     = self.get_endpoint_base("persons")
            json_data    = json.dumps(data)
            headers = self.get_headers_base()
            response = requests.post(url, data=json_data, headers=headers)
            if response.status_code != 200:
                _logger.error(f"\n\nFAILED API CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {str(headers)}\n\t\tData: {str(data)}")
            else:
                _logger.debug(f"\nAPI CALL: {url}\n\tCode: {response.status_code}\n\t\tResponse: {response.text}\n\t\tHeader: {str(headers)}\n\t\tData: {str(data)}")
            return response
        return False

    def post_persons_groups(self, person_id=False, group_id=False, ba_id=False, create_ba=False):
        if person_id and group_id and create_ba:
            r_data = {"role": "user"}
            if ba_id:
                r_data['billingAccount'] = ba_id
            endpoint = self.get_endpoint_base(
                "persons") + "/" + person_id + "/groups/" + group_id+"?createBillingAccount="+create_ba
            r = requests.post(endpoint, data=json.dumps(
                r_data), headers=self.get_headers_base())
            return r
        return False

    def delete_person_group(self, person_id=False, group_id=False):
        if person_id and group_id:
            endpoint = self.get_endpoint_base(
                "persons") + "/" + person_id + "/groups/" + group_id
            response = requests.delete(
                endpoint, headers=self.get_headers_base())
            return response
        return False

    def put_billingaccount_transactions(self, ba_id=False, ttype=False, description=False, amount=False):
        if ba_id and ttype and description and amount:
            endpoint = self.get_endpoint_base(
                "billingAccounts") + "/" + ba_id + "/transactions"
            r_data = {
                "type": ttype,
                "description": description,
                "internalDescription": description,
                "amount": amount
            }
            return requests.put(endpoint, data=json.dumps(r_data), headers=self.get_headers_base())
        return False

    def validate_response(self, response=False):
        if response:
            if response.status_code != 200:
                return False
            return response.json()
        return False

    # def get_reservations_by_group(self,groupid=False,from_q=False,to_q=False):
    #   if groupid and from_q and to_q:
    #     return requests.get
