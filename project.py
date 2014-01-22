#!/usr/bin/env python
#coding: utf-8

# (c) 2007 Sednacom <http://www.sednacom.fr>
# author : gael@sednacom.fr

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
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

from openerp.osv import fields
from openerp.osv import osv
from openerp import tools
from mx import DateTime
from openerp import netsvc

class project(osv.osv):
  _name = "project.project"
  _inherit="project.project"
  _description = "Project with business affair"

  _columns = {
	'business_id' : fields.many2one('business.business','Business', required=False),
	'category_id': fields.many2one('account.analytic.account','Analytic Account'),	
	}

  def onchange_business_id(self, cr, uid, ids, business_id, context=None):
	if not business_id:
		return {}
	analytic = self.pool.get('business.business').browse(cr, uid, business_id, context).analytic_account.id	
	return {'value':{'category_id': analytic}}

project()
