 # -*- coding: utf-8 -*-
##############################################################################
#    
# Module : cd_advanced_invoice
# Author : 2014-03-28 G Lopez @glopzvega
#
# Modulo que permite definir si la venta se factura o no, sustituye a los recibos de cliente
#
##############################################################################

import time
from lxml import etree
import openerp.addons.decimal_precision as dp
import openerp.exceptions

from openerp import netsvc
from openerp import pooler
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class account_invoice(osv.osv):
    
    _inherit = "account.invoice"
    _columns = {
    	# "default_code" : fields.char('Clave', size=13, required=True, help="Clave del Producto"),
    	'invoiced' : fields.boolean("Requiere Factura")    	
    }
    _defaults = {  
    	# 'datee': lambda *a: time.strftime('%Y-%m-%d'),  
    }

account_invoice();

class account_move(osv.osv):
    
    _inherit = "account.move"
    
    #Sobreescritura del metodo post para verificar si el movimiento procede de una factura o recibo
    def post(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        invoice = context.get('invoice', False)
        valid_moves = self.validate(cr, uid, ids, context)

        if not valid_moves:
            raise osv.except_osv(_('Error!'), _('You cannot validate a non-balanced entry.\nMake sure you have configured payment terms properly.\nThe latest payment term line should be of the "Balance" type.'))
        obj_sequence = self.pool.get('ir.sequence')
        for move in self.browse(cr, uid, valid_moves, context=context):
            if move.name =='/':
                new_name = False
                journal = move.journal_id

                if invoice and invoice.internal_number:
                    new_name = invoice.internal_number
                else:
                    if journal.sequence_id:
                        c = {'fiscalyear_id': move.period_id.fiscalyear_id.id}
                        new_name = obj_sequence.next_by_id(cr, uid, journal.sequence_id.id, c)
                    else:
                        raise osv.except_osv(_('Error!'), _('Please define a sequence on the journal.'))

                if new_name:
                    self.write(cr, uid, [move.id], {'name':new_name})
                    
        #Si es factura o recibe influira en si se contabiliza o no el registro.
        if invoice:
        	if invoice.invoiced:
		        cr.execute('UPDATE account_move '\
		                   'SET state=%s '\
		                   'WHERE id IN %s',
		                   ('posted', tuple(valid_moves),))
        else:
        	cr.execute('UPDATE account_move '\
	                   'SET state=%s '\
	                   'WHERE id IN %s',
	                   ('posted', tuple(valid_moves),))	    	    	
        return True

account_move();