# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Vendor views, w/ Quickbooks integration
"""

import json

import colander
from deform import widget as dfwidget
from pyramid.renderers import render
from webhelpers2.html import HTML, tags

from tailbone import grids
from tailbone.views import ViewSupplement


class VendorViewSupplement(ViewSupplement):
    """
    Vendor view supplement for Quickbooks integration
    """
    route_prefix = 'vendors'

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.QuickbooksVendor)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('quickbooks_name', model.QuickbooksVendor.quickbooks_name)
        g.set_filter('quickbooks_bank_account', model.QuickbooksVendor.quickbooks_bank_account)
        g.set_filter('quickbooks_terms', model.QuickbooksVendor.quickbooks_terms)

    def configure_form(self, f):

        # quickbooks_name
        f.append('quickbooks_name')

        # quickbooks_bank_account
        f.append('quickbooks_bank_account')

        # quickbooks_bank_accounts
        f.append('quickbooks_bank_accounts_')
        f.set_renderer('quickbooks_bank_accounts_', self.render_quickbooks_bank_accounts)
        f.set_node('quickbooks_bank_accounts_', BankAccounts())
        f.set_widget('quickbooks_bank_accounts_', BankAccountsWidget(request=self.request))

        # quickbooks_terms
        f.append('quickbooks_terms')

    def render_quickbooks_bank_accounts(self, vendor, field):
        accounts = getattr(vendor, 'quickbooks_bank_accounts')
        if accounts:
            g = make_accounts_grid(self.request)
            return HTML.literal(g.render_table_element(data_prop='quickbooksBankAccountsData'))

    def objectify(self, vendor, form, data):
        model = self.model
        old_accounts = vendor.quickbooks_bank_accounts
        new_accounts = data['quickbooks_bank_accounts_']

        for new_account in new_accounts:
            old_account = old_accounts.get(new_account['store_uuid'])
            if old_account:
                if old_account.account_number != new_account['account_number']:
                    old_account.account_number = new_account['account_number']
            else:
                account = model.QuickbooksVendorBankAccount()
                account.store_uuid = new_account['store_uuid']
                account.account_number = new_account['account_number']
                vendor.quickbooks_bank_accounts[account.store_uuid] = account
                self.Session.add(account)

        final_store_uuids = set([a['store_uuid'] for a in new_accounts])
        for old_account in list(vendor.quickbooks_bank_accounts.values()):
            if old_account.store_uuid not in final_store_uuids:
                self.Session.delete(old_account)

        return vendor

    def template_kwargs(self, **kwargs):
        app = self.get_rattail_app()
        form = kwargs.get('form')
        if form:

            # quickbooks bank accounts
            vendor = kwargs['instance']
            accounts = []
            for account in vendor.quickbooks_bank_accounts.values():
                store = account.store
                accounts.append({
                    'uuid': account.uuid,
                    'store': f'{store.id} - {store.name}',
                    'store_uuid': store.uuid,
                    'store_id': store.id,
                    'store_name': store.name,
                    'account_number': account.account_number,
                })
            accounts.sort(key=lambda a: a['store_id'])
            # nb. this is needed for widget *and* readonly template
            form.set_json_data('quickbooksBankAccountsData', accounts)
            # TODO: these are needed by widget
            stores = []
            for store in app.get_active_stores(self.Session()):
                stores.append({
                    'uuid': store.uuid,
                    'display': f'{store.id} - {store.name}',
                })
            form.include_template('/vendors/quickbooks_bank_accounts_js.mako', {
                'store_options': stores,
            })

        return kwargs

    def get_version_child_classes(self):
        model = self.model
        return [model.QuickbooksVendor]


def make_accounts_grid(request):
    g = grids.Grid('quickbooks_bank_accounts',
                   request=request,
                   data=[],         # empty data
                   columns=[
                       'store',
                       'account_number',
                   ])
    return g


class BankAccount(colander.MappingSchema):

    store_uuid = colander.SchemaNode(colander.String())

    account_number = colander.SchemaNode(colander.String())


class BankAccounts(colander.SequenceSchema):

    account = BankAccount()


class BankAccountsWidget(dfwidget.Widget):

    def serialize(self, field, cstruct, **kw):
        g = make_accounts_grid(self.request)

        g.main_actions.append(
            grids.GridAction('edit', icon='edit',
                             click_handler='quickbooksBankAccountEdit(props.row)'))

        g.main_actions.append(
            grids.GridAction('delete', icon='trash',
                             click_handler='quickbooksBankAccountDelete(props.row)'))

        widget = render('/vendors/quickbooks_bank_accounts_widget.mako', {
            'grid': g,
        })

        return HTML.tag('div', c=[
            HTML.literal(widget),
            tags.hidden(field.name, **{':value': "quickbooksBankAccountsFinal"}),
        ])

    def deserialize(self, field, pstruct):
        return json.loads(pstruct)


def includeme(config):
    VendorViewSupplement.defaults(config)
