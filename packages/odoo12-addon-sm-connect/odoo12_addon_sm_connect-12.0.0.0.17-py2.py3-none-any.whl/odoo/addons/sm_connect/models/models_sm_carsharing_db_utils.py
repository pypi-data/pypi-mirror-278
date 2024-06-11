# -*- coding: utf-8 -*-

import firebase_admin
from firebase_admin import auth as fire_auth, credentials, db


def get_firebase_priv_auth_credentials(company):
    return {
        "type": company.sm_firebase_auth_type,
        "project_id": company.sm_firebase_auth_project_id,
        "private_key_id": company.sm_firebase_auth_private_key_id,
        "private_key": company.sm_firebase_auth_private_key.replace('\\n', '\n'),
        "client_email": company.sm_firebase_auth_client_email,
        "client_id": company.sm_firebase_auth_client_id,
        "auth_uri": company.sm_firebase_auth_auth_uri,
        "token_uri": company.sm_firebase_auth_token_uri,
        "auth_provider_x509_cert_url": company.sm_firebase_auth_provider_x509,
        "client_x509_cert_url": company.sm_firebase_auth_client_x509,
    }


class sm_carsharing_db_utils(object):
    __instance = None
    __cred = None
    __sm_carsharing_app = None

    @staticmethod
    def get_instance(parent):
        if sm_carsharing_db_utils.__instance is None:
            sm_carsharing_db_utils(parent)

        token_info = sm_carsharing_db_utils.__cred.get_access_token()
        cred_info = sm_carsharing_db_utils.__cred.get_credential()

        token_is_expired = cred_info.expired

        if token_is_expired:
            firebase_admin.delete_app(
                app=sm_carsharing_db_utils.__sm_carsharing_app)
            company = parent.env.user.company_id
            credentials_fire_priv = get_firebase_priv_auth_credentials(company)

            sm_carsharing_db_utils.__cred = credentials.Certificate(
                credentials_fire_priv)

            sm_carsharing_db_utils.__sm_carsharing_app = firebase_admin.initialize_app(
                sm_carsharing_db_utils.__cred,
                {'databaseURL': company.sm_firebase_auth_db_ref}
            )

        return sm_carsharing_db_utils.__instance

    def __init__(self, parent):
        if sm_carsharing_db_utils.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            sm_carsharing_db_utils.__instance = self

        company = parent.env.user.company_id
        credentials_fire_priv = get_firebase_priv_auth_credentials(company)

        sm_carsharing_db_utils.__cred = credentials.Certificate(
            credentials_fire_priv)

        sm_carsharing_db_utils.__sm_carsharing_app = firebase_admin.initialize_app(
            sm_carsharing_db_utils.__cred,
            {'databaseURL': company.sm_firebase_auth_db_ref}
        )

    def firebase_get(self, endpoint, key=False):
        if key:
            query = db.reference(path=endpoint).child(path=key)
        else:
            query = db.reference(path=endpoint)
        result = query.get()
        return result

    def firebase_put(self, endpoint, key, data):
        ref = db.reference(path=endpoint)
        key_child = ref.child(path=key)
        key_child.set(data)

    def firebase_update(self, endpoint, key, data):
        ref = db.reference(path=endpoint)
        key_child = ref.child(path=key)
        key_child.update(data)

    def firebase_delete(self, endpoint=None, key=None):
        ref = db.reference(path=endpoint)
        key_child = ref.child(path=key)
        key_child.delete()

    def delete_user_from_auth(self, uid=None):
        fire_auth.delete_user(uid, app=self.__sm_carsharing_app)

    def get_uid_from_email(self, email):
        try:
            firebase_user_info = fire_auth.get_user_by_email(
                email, app=self.__sm_carsharing_app)
            return firebase_user_info.uid
        except:
            return False
