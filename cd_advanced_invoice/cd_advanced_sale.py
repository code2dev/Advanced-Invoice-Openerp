 # -*- coding: utf-8 -*-
##############################################################################
#    
# Module : cd_advanced_invoice
# 
# Modulo que permite definir si la venta se factura o no, sustituye a los recibos de cliente
#
##############################################################################

import openerp
from openerp.osv import osv, fields

class sale_order(osv.osv):
    
    _inherit = "sale.order"
    _columns = {
    	# "default_code" : fields.char('Clave', size=13, required=True, help="Clave del Producto"),    	
        "invoice_required" : fields.boolean("Requiere Factura")
    }

    _defaults = {  
        'invoice_required': True,  
    }

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
    	invoice_vals = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context=context)
    	invoice_vals.update({"invoiced" : order.invoice_required})
    	return invoice_vals

sale_order();