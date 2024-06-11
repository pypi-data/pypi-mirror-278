# -*- coding: utf-8 -*-
{
    'name': "sm_connect",

    'summary': """
    Connect odoo to other apps like wordpress, firbase or carsharing app
  """,

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': 'vertical-carsharing',
    'version': '12.0.0.0.17',

    # any module necessary for this one to work correctly
    'depends': [
      'base',
      'web',
      'vertical_carsharing',
      'sm_carsharing_structure_sommobilitat',
    ],

    # always loaded
    'data': [
        'views/form_view_controller.xml',
        'views/views_res_config_settings.xml',
        'views/views_fleetio_car.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
