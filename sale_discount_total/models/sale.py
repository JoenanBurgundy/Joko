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
    
    @api.depends('discount', 'amount_untaxed')
    def _get_amount_discount(self):
        for sale in self:
            sale.amount_bfr_discount = sum([line.product_uom_qty * line.price_unit for line in sale.order_line])
            sale.amount_discount = sum([line.product_uom_qty * line.price_unit for line in sale.order_line]) * sale.discount / 100
    
    discount = fields.Float(string='Discount (%)', states={'draft': [('readonly', False)]})
    amount_discount = fields.Float(string='Discount', compute='_get_amount_discount')
    amount_bfr_discount = fields.Float(string='Before Discount', compute='_get_amount_discount')

    @api.multi
    @api.onchange('discount')
    def onchange_discount(self):
        for line in self.order_line:
            line.discount = self.discount
        return {}
