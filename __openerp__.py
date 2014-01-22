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


{
    'name': 'Module business',
    'version': '0.1',
    'category': 'Generic Modules/Others',
    'description': """
This module regroup object for a business.
This is just a test of git VCS (Version Control Systems)""",
    'author': 'Sednacom',
    'website': 'http://www.sednacom.fr',
    'depends': ['account', 'analytic', 'crm', 'sale', 'purchase', 'project', 'hr_timesheet'], #'contacts'
    'data': [
        #'security/business_security.xml',
        #'security/ir.model.access.csv',
        'business_sequence.xml',
        'business_data.xml',
        'res_partner_view.xml',
        'product_view.xml',
        'business_view.xml',
        'business_menu.xml',
        'report/business_report_view.xml',
    ],
    'demo': [],
    'test':[],
    'installable': True,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
