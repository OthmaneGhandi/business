# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _

class product_product(osv.osv):
    _name='product.product'
    _inherit='product.product'

    def onchange_business_product_ok(self, cr, uid, ids, business_product_ok, context=None):
        result = {'business_system_ok': False, 'business_product_ok': False}
        if business_product_ok:
            result.update({'business_product_ok': True})
        return {'value': result}

    def onchange_business_system_ok(self, cr, uid, ids, business_system_ok, context=None):
        result = {'business_system_ok': False, 'business_product_ok': False}
        if business_system_ok:
            result.update({'business_system_ok': True})
        return {'value': result}
    
    _columns={
              'business_product_ok': fields.boolean(u'Equipement'),
              'business_system_ok': fields.boolean(u'Système'),
              'product_business_id': fields.many2one('business.business', u'Equip Bus Id'),
              'system_business_id': fields.many2one('business.business', u'Sys Bus Id'),
             }
product_product()

class product_market_combination(osv.osv):
    _name = 'product.market.combination'
    _description = 'Product Market Combination'

    _columns = {
                'name': fields.char(u'Code', size=64, required=True),
                'description': fields.text(u'Description'),
                'pmc_line_ids': fields.one2many('product.market.combination.line', 'pmc_id', u'Sous-familles')
               }
product_market_combination()

class product_market_combination_line(osv.osv):
    _name = 'product.market.combination.line'
    _description = 'Sous-familles PMC'

    _columns = {
                'pmc_id': fields.many2one('product.market.combination', u'PMC id'),
                'name': fields.char(u'Code', size=64, required=True),
                'description': fields.text(u'Description'),
               }
product_market_combination_line()
