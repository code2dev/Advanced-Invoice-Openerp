# -*- coding: utf-8 -*-
{
    'name': 'Gestion Avanzada de Facturas y Recibos',
    'version': '1.0.0',
    'category': 'Account',
    'sequence': 3,
    'author': 'Gerardo A Lopez Vega',
    'website': 'http://codetodev.com',
    'summary': 'Permite elegir si la venta se factura o solo se genera recibo',
    'description': "Permite elegir si la venta se factura o solo se genera recibo, gestionando asi la contabilidad de dicho registro, cuando es recibo el registro no se contabiliza, ambos registros se visualizan en Facturas de Cliente",
    'depends': ["account", "sale"],
    'data': [        
         'cd_advanced_invoice_view.xml',
         'cd_advanced_sale_view.xml',
    ],    
    'installable': True,
    'application': False,
    'auto_install': False,
}