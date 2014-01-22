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

from openerp.osv import fields,osv
from openerp import tools

MONTHS = [
    ('01', 'January'),
    ('02', 'February'),
    ('03', 'March'),
    ('04', 'April'),
    ('05', 'May'),
    ('06', 'June'),
    ('07', 'July'),
    ('08', 'August'),
    ('09', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December')
]

class report_affaire_equipment_user(osv.osv):
    _name = "report.affaire.equipment.user"
    _description = "equipments by user and product"
    _auto = False
    _columns = {
         'name_template': fields.char('product summary', size=128, readonly=True),
         'country': fields.char('Pays', size=128, readonly=True),
         'region': fields.char('Région', size=128, readonly=True),
         'business_product_ok': fields.boolean(u'Equipement'),
         'business_system_ok': fields.boolean(u'Système'),
         'business_id': fields.many2one('business.business', 'Affaire', readonly=True),
         'sys_business_id': fields.many2one('business.business', 'sys_Affaire', readonly=True),
         'product_qty_planned': fields.float(u'Quantité prévue'),
         'product_qty_used': fields.float(u'Quantité utilisée'),         
         'nbr': fields.integer('NB de produit', readonly=True),
         'creation_year': fields.char('Creation Year', size=10, readonly=True, help="Creation year"),
         'creation_month': fields.selection(MONTHS, 'Creation Month', readonly=True, help="Creation month"),
         'creation_day': fields.char('Creation Day', size=10, readonly=True, help="Creation day"),         
         
    }
    _order = 'name_template desc, business_id, sys_business_id'

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'report_affaire_equipment_user')
        cr.execute("""
            CREATE view report_affaire_equipment_user as
              SELECT
                    (select 1 ) AS nbr,
                    t.id AS id,
                    t.product_business_id AS business_id,
                    t.system_business_id AS sys_business_id,
                    t.product_qty_planned AS product_qty_planned,
                    t.product_qty_used AS product_qty_used,
                    s.name_template as name_template,
                    s.business_product_ok AS business_product_ok,
                    s.business_system_ok AS business_system_ok,
                    
                    r.name AS country,
                    b.region AS region,

                    to_char(b.date_prob, 'YYYY') as creation_year,
                    to_char(b.date_prob, 'MM') as creation_month,
                    to_char(b.date_prob, 'YYYY-MM-DD') as creation_day                    
              FROM business_product t, product_product s, business_business b, res_country r
              WHERE (t.product_id = s.id) and (t.product_business_id = b.id or t.system_business_id = b.id) and (b.country_id = r.id)
                GROUP BY
                 t.id,
                 business_id,
                 sys_business_id,
                 business_product_ok,
                 business_system_ok,
                 name_template,
                 country,
                 region,
                 creation_year,
                 creation_month,
                 creation_day

        """)

report_affaire_equipment_user()

