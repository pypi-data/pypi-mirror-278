# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_company(models.Model):
    _inherit = 'res.company'

    ''' CS API Credentials '''
    sm_carsharing_api_credentials_api_key = fields.Char(
        string=_("Carsharing API Key"))
    sm_carsharing_api_credentials_cs_url = fields.Char(
        string=_("Carsharing API URL"))
    sm_carsharing_api_credentials_admin_group = fields.Char(
        string=_("Carsharing Admin Group"))

    ''' WORDPRESS DB CREDENTIALS '''
    sm_wordpress_db_credentials_admin_host = fields.Char(
        string=_("Wordpress DB Admin Host"))
    sm_wordpress_db_credentials_admin_username = fields.Char(
        string=_("Wordpress DB Admin Username"))
    sm_wordpress_db_credentials_admin_password = fields.Char(
        string=_("Wordpress DB Admin Password"))
    sm_wordpress_db_credentials_db_host = fields.Char(
        string=_("Wordpress DB Host"))
    sm_wordpress_db_credentials_db_username = fields.Char(
        string=_("Wordpress DB Username"))
    sm_wordpress_db_credentials_db_password = fields.Char(
        string=_("Wordpress DB Password"))
    sm_wordpress_db_credentials_db_database = fields.Char(
        string=_("Wordpress DB Database"))

    ''' FIREBASE AUTH CREDENTIALS '''
    sm_firebase_auth_type = fields.Char(string=_("Firebase Auth Type"))
    sm_firebase_auth_project_id = fields.Char(
        string=_("Firebase Auth Project ID"))
    sm_firebase_auth_private_key_id = fields.Char(
        string=_("Firebase Auth Private Key ID"))
    sm_firebase_auth_private_key = fields.Char(
        string=_("Firebase Auth Private Key"))
    sm_firebase_auth_client_email = fields.Char(
        string=_("Firebase Auth Client Email"))
    sm_firebase_auth_client_id = fields.Char(
        string=_("Firebase Auth Client ID"))
    sm_firebase_auth_auth_uri = fields.Char(string=_("Firebase Auth URI"))
    sm_firebase_auth_token_uri = fields.Char(
        string=_("Firebase Auth Token URI"))
    sm_firebase_auth_provider_x509 = fields.Char(
        string=_("Firebase Auth Provider X509"))
    sm_firebase_auth_client_x509 = fields.Char(
        string=_("Firebase Auth Client X509"))
    sm_firebase_auth_db_ref = fields.Char(
        string=_("Firebase Database Reference"))
    
    ''' Fleetio API Credentials '''
    sm_fleetio_api_token = fields.Char(
        string=_("Fleetio API Token"))
    sm_fleetio_account_token = fields.Char(
        string=_("Fleetio Account Token"))
    sm_fleetio_test_mode = fields.Boolean(
        string=_("Fleetio Testing Mode"),
        help=_("Enabling Test Mode will create the new vehicles with Test_<NAME> and inactive by default"))
