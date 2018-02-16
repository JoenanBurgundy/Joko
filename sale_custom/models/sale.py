import datetime
from datetime import date
# from datetime import timedelta
# from dateutil import relativedelta
# import time

from odoo import models, fields, api, _
from openerp.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
# from openerp.tools.safe_eval import safe_eval as eval
# from openerp.tools.translate import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.depends('bank_charge', 'amount_untaxed', 'fee')
    def _get_commission(self):
        for order in self:
            order.commission_amount = order.amount_untaxed - (order.bank_charge + order.fee)
            
    @api.depends('partner_id')
    def _get_partner_sale(self):
        for order in self:
            sale_ids = self.search([
                ('partner_id', '=', order.partner_id.id),
                ('date_order', '<', order.date_order),
                ('state', 'in', ('sale', 'done'))
            ])
            order.partner_order_count = len(sale_ids)

    partner_order_count = fields.Integer(string='Repeat Order',
                                         compute='_get_partner_sale', store=True)
    commission_amount = fields.Float(string='Commission', compute='_get_commission', store=True)
    bank_charge = fields.Float(string='Bank Charge')
    fee = fields.Float(string='Fee')

    @api.multi
    @api.onchange('date_order')
    def onchange_validity_date(self):
        date = datetime.datetime.strptime(self.date_order, DEFAULT_SERVER_DATETIME_FORMAT)
        new_date = date + datetime.timedelta(days=14)
        self.validity_date = new_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return {}
