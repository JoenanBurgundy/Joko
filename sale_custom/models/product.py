from datetime import date
from datetime import datetime
# from datetime import timedelta
# from dateutil import relativedelta
# import time

from odoo import models, fields, api, _
from openerp.exceptions import UserError
# from openerp.tools.safe_eval import safe_eval as eval
# from openerp.tools.translate import _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        if vals.get('name', False):
            name_list = vals.get('name').split(' ')
            first_name_up = name_list[0].upper()
            name_list[0] = first_name_up
            new_name = ' '.join(name_list)
            vals['name'] = new_name
        return super(ProductTemplate, self).create(vals)
    
