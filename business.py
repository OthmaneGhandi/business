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

###################################
AVAILABLE_STATES = [
    ('0', u'0'),
    ('10', u'10'),
    ('20', u'20'),
    ('30', u'30'),
    ('40', u'40'),
    ('50', u'50'),
    ('60', u'60'),
    ('70', u'70'),
    ('80', u'80'),
    ('90', u'90'),
    ('100', u'100'),
]


def _default_purchase_analytic( obj, cr, uid, context):
    #print '_default_purchase_analytic',context
    business_id = context.get( 'business_id', False )
    if business_id:
        res = obj.pool.get( 'business.business' ).browse( cr, uid, business_id, context ).analytic_account.id
    else:
        res = False
    #purchase_order_obj = obj.pool.get('purchase.order').browse( cr, uid, context )
    #print purchase_order_obj
    return res

class business_business(osv.osv):
    _name = "business.business"
    _description = "business affair"


    def create(self, cr, uid, vals, context=None):
        if ('name' not in vals) or (vals.get('name')=='/'):
            seq_obj_name= 'business.business'
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, seq_obj_name)
        return super(business_business, self).create(cr, uid, vals, context)
    
    def onchange_qty_used(self, cr, uid, ids, percentage, context=None):
        business = self.browse(cr,uid,ids,context=context)
        if business:
            business_id = business[0].id
            product_ids = self.pool.get('business.product').search(cr, uid, [('product_business_id','=',business_id)])
            for product_id in self.pool.get('business.product').browse(cr,uid,product_ids,context=context):
                value = {}
                qty_used = product_id.product_qty_planned * percentage
                qty_used = qty_used / 100
                value['product_qty_used'] = qty_used
#            vals = (1, product_id.id, { 'product_qty_used': qty_used })
                self.pool.get('business.product').write(cr, uid, [product_id.id], value, context=context)         
        return True    

    def button_reset_qty_used(self, cr, uid, ids, context=None):
        business = self.browse(cr,uid,ids,context=context)
        if business:
            business_id = business[0].id
            product_ids = self.pool.get('business.product').search(cr, uid, [('product_business_id','=',business_id)])
            for product_id in self.pool.get('business.product').browse(cr,uid,product_ids,context=context):
                value = {}
                percentage = business[0].percentage
                qty_used = product_id.product_qty_planned * percentage
                qty_used = qty_used / 100
                value['product_qty_used'] = qty_used
#            vals = (1, product_id.id, { 'product_qty_used': qty_used })
                self.pool.get('business.product').write(cr, uid, [product_id.id], value, context=context)         
        return True     

    def onchange_pmc_id(self, cr, uid, ids, pmc_id, context=None):
        domain, result = {}, {'pmc_line_id': False}
        if pmc_id:
            pmc_line_ids = self.pool.get('product.market.combination.line').search(cr, uid, [('pmc_id','=',pmc_id)])
            domain.update({'pmc_line_id': [('id','in',pmc_line_ids)]})
            if len(pmc_line_ids) == 1:
                result.update({'pmc_line_id': pmc_line_ids[0]})
	    return {'value': result, 'domain': domain}
    
    def onchange_contact_id(self, cr, uid, ids, contact_id, context=None):
        result = {'contact': ""}
        if contact_id:
            partner_datas = self.pool.get('res.partner').read(cr, uid, contact_id, ['phone','mobile'])
            result.update({'contact': partner_datas['phone'] and (partner_datas['phone']+" / "+ (partner_datas['mobile'] or "")) or partner_datas['mobile'] or ""})
        return {'value': result}
    
    def onchange_onduline_ok(self, cr, uid, ids, onduline_ok, context=None):
        result = {'date_prob': False}
        return {'value': result}

    def make_list_partners(self, cr, uid, ids,business, arg, context):	
	    for busi in self.browse(cr, uid, ids):
		    business_id = busi.name
	    res1=[]	
	    if business_id:
		    crit = [('business_id','=',business_id)]		
		    res2 = self.pool.get('sale.order').search(cr, uid, crit)	
		    for sale in self.pool.get('sale.order').browse(cr, uid, res2):
			    res1.append(sale.partner_id.id)		
		    res3 = self.pool.get('purchase.order').search(cr, uid, crit)		
		    for purchase in self.pool.get('purchase.order').browse(cr, uid, res3):
			    res1.append(purchase.partner_id.id)			
		    res = list(set(res1))
		    print res		
	    else:
		    return False
	    return res
    
    def _get_default_user(self, cr, uid, context=None):
        return uid

    _columns = {
	            'name' : fields.char(u'Séquence', size=64, required=True, readonly=True),
	            'description' : fields.char(u'Nom', size=64, required=True),
                'color': fields.integer(u'Couleur'),
                'user_id': fields.many2one('res.users', 'Utilisateur', select=True, track_visibility='onchange'),
                'pmc_id': fields.many2one('product.market.combination', u'PMC', required=True),
                'pmc_line_id': fields.many2one('product.market.combination.line', u'Sous-type PMC'),
                'affair_location': fields.char(u'Lieu de l\'affaire', size=32, required=True),
                'contact': fields.one2many('res.partner', 'business_id', 'Contact(s)'),
                'contact_id': fields.one2many('res.partner', 'business_id', 'Partner(s)'),
                'promo_id': fields.one2many('res.partner', 'business_id', 'Financement/Promoteur'),
                'country_id': fields.many2one('res.country', u'Pays', required=True),    
                'region' : fields.char(u'Région', size=64, required=True),            
                #'products': fields.one2many('product.product', 'product_business_id', u'Equipements'),
                #'systems': fields.one2many('product.product', 'system_business_id', u'Systèmes'),
                'products': fields.one2many('business.product', 'product_business_id', u'Equipements'),
                'systems': fields.one2many('business.product', 'system_business_id', u'Systèmes'),
                'plannings': fields.one2many('business.planning', 'business_id', u'Planning de réalisation'),
                #'plan': fields.selection([('toit',u'TOITURE'),('bat',u'BATIMENT')]),
                'onduline_ok': fields.boolean(u'Onduline spécifié'),
                #'products_volume': fields.float(u'Volume des équipements'),
                #'systems_volume': fields.float(u'Volume des systèmes'),
                #'vol_uom_id': fields.many2one('product.uom', u'Unité de mesure', help=u"Unité de mesure des équipements."),
                'date_prob': fields.date(u'Date probable de démarrage'),
                'business_need': fields.selection([('equip',u'Equipements'),('syst',u'Systèmes')], u'Besoins'),
                'hunting_pack_ok': fields.boolean(u'Hunting pack'),
                'tech_partners': fields.one2many('business.tech.partner', 'business_id', u'Partenaires & Technologies'),
	            'date_start': fields.date('Date de début'),
	            'date_end': fields.date('Date de fin'),
	            'analytic_account' : fields.many2one('account.analytic.account', 'Compte analytique',required=False),
	            #'list_partners' : fields.one2many('partner.from.list', 'business_id', 'Sale', readonly=True),
	            'sales' : fields.one2many('sale.order', 'business_id', 'Sales'),
	            'purchases' : fields.one2many('purchase.order', 'business_id', 'Purchases'),
	            'invoices' :fields.one2many('account.invoice', 'business_id', 'Invoices'),
    	        'projects' : fields.one2many('project.project', 'business_id', 'Projects'),
                'state': fields.many2one('business.state', 'Etat du projet', required=True),
                'percentage': fields.integer(u'Pourcentage', required=True),
	            }

    _defaults={
               'name': '/',
               'color': 0,
               'percentage': 100,            
               'user_id': lambda s, cr, uid, c: s._get_default_user(cr, uid, c),
               #'business_need': 'all',
              }

business_business()

# Classe pour enregistrer les états d'une affaire

class business_state(osv.osv):
    _name = "business.state"
    _description = u"Etat de l'affaire"
    
    _columns={
              'name': fields.char(u'Etats', size=64, required=True),
              'percentage': fields.integer(u'Pourcentage', required=True),
             }

business_state()

class business_product(osv.osv):
    _name = "business.product"
    _description = u"Produits et Systèmes Business"
         
    
#     def onchange_qnty_used(self, cr, uid, ids, product_qty_planned, context=None):
#         result = {'product_qty_used': 0.0}
#         product = self.browse(cr,uid,ids,context=context)
#         if product:
#             business_id = product[0].product_business_id
#             print 'business id', business_id
#             if business_id:
#                     business = self.pool.get('business.business').browse(cr,uid,[business_id],context=context)
#                     print 'business id ********', business[0]
#                     perctg = business[0].region
#                     print 'Pourcentage *******', perctg
# #                    qty_used = product_qty_planned * percentage
# #                    qty_used = qty_used / 100
# #                    result.update({'product_qty_used': qty_used})
#         return {'value': result}
# 
#     def onchange_qanty_used(self, cr, uid, ids, product_qty_planned, context=None):
#         
#         for product_id in self.browse(cr,uid,ids,context=context):
#             if product_id.product_business_id:
#                 value = {}
#                 business_id = product_id.product_business_id
#                 business = self.pool.get('business.business').browse(cr,uid,[business_id],context=context)
#                 print 'business <=================>', business
#                 percentage = business[0].percentage
#                 print 'pourcentage <=================>', percentage
#                 qty_used = product_qty_planned * percentage
#                 qty_used = qty_used / 100
#                 value['product_qty_used'] = qty_used
#                 self.pool.get('business.product').write(cr, uid, [product_id.id], value, context=context)                         
#         return True
     
#############################################################################################################
    
    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        result = {'product_qty_planned': 0.0, 'price': 0.0, 'uom_id': False}
        if product_id:
            product_datas = self.pool.get('product.product').read(cr, uid, product_id, ['list_price','uom_id'])
            result.update({'price': product_datas['list_price'], 'uom_id': product_datas['uom_id'][0]})
        return {'value': result}
    
    _columns={
              'product_business_id': fields.many2one('business.business', u'Product Business id'),
              'system_business_id': fields.many2one('business.business', u'System Business id'),
              'product_id': fields.many2one('product.product', u'Produit'),
              'price': fields.float(u'Prix de vente'),
              'uom_id': fields.many2one('product.uom', u'UdM', required=True, help=u"Unité de mesure du produit."),
              'product_qty_planned': fields.float(u'Quantité prévue'),
#              'product_qty_used': fields.function(_get_qty_used, method=True, type='float', string='Quantité utilisée',store=True ),
              'product_qty_used': fields.float(u'Quantité utilisée'),
             }
    _defaults = {
                 'product_qty_planned': 1.0,
               
                 }

business_product()

class business_formation(osv.osv):
    _name="business.formation"
    _description="Formation"
    
    _columns={
              'center_id': fields.many2one('business.training.center', u'Training center'),
              'trainer_cost_ids': fields.one2many('business.trainer.cost', 'formation_id', u'Master Trainers'),
              'trainee_ids': fields.one2many('hr.employee', 'formation_id', u'Charpentiers formés'),
              'formation_plan_ids': fields.one2many('business.formation.plan', 'formation_id', u'Plan de formation'),
              }
business_formation()

class hr_employee(osv.osv):
    _name="hr.employee"
    _inherit="hr.employee"
    
    _columns={
              'formation_id': fields.many2one('business.formation', u'Formation ref'),
              }
hr_employee()

class business_trainer_cost(osv.osv):
    _name="business.trainer.cost"
    _description="Cost"
    
    _columns={
              'formation_id': fields.many2one('business.formation', u'Formation ref'),
              'trainer_id': fields.many2one('res.partner', u'Master trainer', domain="[('business_trainer_ok','=',True)]", required=True),
              'level': fields.char(u'Niveau', size=64, required=True),
              'cost': fields.float(u'Coût', required=True),
              }
business_trainer_cost()

class business_formation_plan(osv.osv):
    _name="business.formation.plan"
    _description="Plan de formation"
    
    _columns={
              'formation_id': fields.many2one('business.formation', u'Formation ref'),
              'employee_type': fields.selection([('charp', u'Charpentiers'),('couv', u'Couvreurs')], u'Type d\'employé', required=True),
              'qty': fields.integer(u'Quantité', required=True),
              'date': fields.datetime(u'Date de formation', required=True),
              }
business_formation_plan()

class business_tech_partner(osv.osv):
    _name = "business.tech.partner"
    _description = u"Partenaires et Technologies"
    
    _columns={
              'business_id': fields.many2one('business.business', u'Business id'),
              'partner_id': fields.many2one('res.partner', u'Partenaire'),
              'product_id': fields.many2one('product.product', u'Technologie'),
              'disposition': fields.text(u'Dispositions spécifiques'),
             } 

business_tech_partner()

class business_planning(osv.osv):
    _name = "business.planning"
    _description = "Planning de réalisation"
    
    _columns={
              'business_id': fields.many2one('business.business', u'Business id'),
              'type': fields.selection([('toiture',u'Toiture'),('batiment',u'Bâtiment')], u'Type', required=True),
              'qty': fields.integer(u'Quantité'),
              'plan': fields.selection([('toit',u'TOITURE'),('bat',u'BATIMENT')], u'Plans'),
             } 

business_planning()

class business_training_center(osv.osv):
    _name = "business.training.center"
    _description = "business training center"

    _columns={
              'partner_id': fields.many2one('res.partner', u'Responsable', required=True),
              'stock_goodies': fields.integer(u'stock goodies', help="Lié au nombre de charpentiers à former par an."),
             }

business_training_center()

class sale_order(osv.osv):
  _name = "sale.order"
  _inherit = "sale.order"
  _description = "Sale order with business affair"

  _columns = {
	'business_id' : fields.many2one('business.business','Business', required=False),
	}

  def onchange_business_id(self, cr, uid, ids, business_id, context=None):
	if not business_id:
		return {}
	analytic = self.pool.get('business.business').browse(cr, uid, business_id, context).analytic_account.id	
	return {'value':{'project_id': analytic}}

  def action_invoice_create(self, cr, uid, ids, grouped=False, states=['confirmed','done']):
		res = super(sale_order, self).action_invoice_create(cr, uid, ids, grouped, states)			
		for o in self.browse(cr, uid, ids):		
			inv = self.pool.get('account.invoice').write(cr, uid, [res], {'business_id': o.business_id.id})		
		return res
sale_order()

class purchase_order(osv.osv):
  _name = "purchase.order"
  _inherit = "purchase.order"
  _description = "Purchase order with business affair"

  _columns = {
	'business_id' : fields.many2one('business.business','Business', required=False),
    'analytic_account_id' : fields.many2one('account.analytic.account', 'Analytic Account',required=False,invisible=True),
	}

  def onchange_business_id(self, cr, uid, ids, business_id, context=None):
    if not business_id:
        return {}
    analytic_id = self.pool.get('business.business').browse(cr, uid, business_id, context).analytic_account.id    
    return {'value':{'account_analytic_id': analytic_id}}

  def action_invoice_create(self, cr, uid, ids, *args):
		res = super(purchase_order, self).action_invoice_create(cr, uid, ids, *args)		
		for o in self.browse(cr, uid, ids):		
			inv = self.pool.get('account.invoice').write(cr, uid, [res], {'business_id': o.business_id.id})		
		return res
purchase_order()

#class purchase_order_line(osv.osv):
#  _name = "purchase.order.line"
#  _inherit = "purchase.order.line"
#  _description = "purchase order line with business affair"

#  _defaults={
#	'account_analytic_id' : lambda *args : _default_purchase_analytic( *args ) , 
#            }
#purchase_order_line()

class account_invoice(osv.osv):
  _name = "account.invoice"
  _inherit = "account.invoice"
  _description = "invoice with business affair"

  _columns = {
	'business_id' : fields.many2one('business.business','Business', required=False),
	}

account_invoice()

class partner_from_sale(osv.osv):
	_name = "partner.from.sale"
	_description = "Partners from business sales"
	_order='partner_id'
	_auto = False
	_columns = {
		'name': fields.one2many('sale.order', 'business_id', 'Sale Order', readonly=True),
		'business_id': fields.many2one('business.business','Business'),
		'partner_id' : fields.many2one('res.partner','Partner'),
	}
	def init(self, cr):
		cr.execute("""
			create or replace view partner_from_sale as (
				select
					id, partner_id,business_id,name 
						from 
							sale_order 
						)""")
partner_from_sale()

class partner_from_purchase(osv.osv):
	_name = "partner.from.purchase"
	_description = "Partners from business purchases"
	_order='partner_id'
	_auto = False
	_columns = {
		'name': fields.one2many('purchase.order', 'business_id', 'Purchase Order', readonly=True),
		'business_id': fields.many2one('business.business','Business'),
		'partner_id' : fields.many2one('res.partner','Partner'),
	}
	def init(self, cr):
		cr.execute("""
			create or replace view partner_from_purchase as (
				select
					id, partner_id,business_id,name 
						from 
							purchase_order 
						)""")
partner_from_purchase()

class partner_from_invoice(osv.osv):
	_name = "partner.from.invoice"
	_description = "Partners from business invoices"
	_order='partner_id'
	_auto = False
	_columns = {
		'name': fields.one2many('account_invoice', 'business_id', 'Purchase Order', readonly=True),
		'business_id': fields.many2one('business.business','Business'),
		'partner_id' : fields.many2one('res.partner','Partner'),
	}
	def init(self, cr):
		cr.execute("""
			create or replace view partner_from_invoice as (
				select
					id, partner_id,business_id,name 
						from 
							account_invoice 
						)""")
partner_from_invoice()

class partner_from_list(osv.osv):
	_name = "partner.from.list"
	_description = "Partners from business"
	_order='partner_id'
	_auto = False
	_columns = {
		'business_id': fields.many2one('business.business','Business'),		
		'partner_id' : fields.many2one('res.partner','Partner'),
	}
	def init(self, cr):
		cr.execute("""
			create or replace view partner_from_list as (
				SELECT DISTINCT r.id,r.id as partner_id,b.id as business_id
					FROM res_partner r, business_business b, 
						partner_from_invoice i, partner_from_sale s,
						partner_from_purchase p
					WHERE b.id=p.business_id and b.id=s.business_id and b.id=i.business_id
						)""")
partner_from_list()

class res_partner(osv.osv):
  _name = "res.partner"
  _inherit = "res.partner"
  _description = "extension of res_partner view"

  _columns = {
    'partner': fields.boolean(u'partner'),
    'business_id': fields.many2one('business.business', u'Business id'),
    }

res_partner()

class project_project(osv.osv):
  _name = "project.project"
  _inherit = "project.project"
  _description = "extension of project view"

  _columns = {
     'description': fields.text(u'Description'),
    }

res_partner()