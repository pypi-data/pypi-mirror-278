# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
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
Views for Quickbooks invoices
"""

import logging

from rattail_quickbooks.db.model import (QuickbooksExportableInvoice,
                                         QuickbooksExportableInvoiceDistribution,
                                         QuickbooksInvoiceExport)
from rattail.threads import Thread
from rattail.util import simple_error

import colander
from pyramid.httpexceptions import HTTPFound

from tailbone import forms
from tailbone.views import MasterView
from tailbone.views.exports import ExportMasterView


log = logging.getLogger(__name__)


class ToggleInvoices(colander.MappingSchema):
    uuids = colander.SchemaNode(colander.String())


class ExportableInvoiceView(MasterView):
    """
    Master view for Quickbooks exportable invoices
    """
    model_class = QuickbooksExportableInvoice
    route_prefix = 'quickbooks.exportable_invoices'
    url_prefix = '/quickbooks/exportable-invoices'
    editable = False
    bulk_deletable = True
    has_versions = True

    labels = {
        'store_id': "Store ID",
        'vendor_id': "Vendor ID",
        'txn_id': "Transaction ID",
        'quickbooks_vendor_terms': "Vendor Terms",
        'quickbooks_export_template': "Export Template",
        'status_code': "Status",
    }

    grid_columns = [
        'invoice_date',
        'invoice_number',
        'invoice_total',
        'store',
        'vendor',
        'quickbooks_vendor_terms',
        'quickbooks_export_template',
        'status_code',
    ]

    form_fields = [
        'store',
        'vendor',
        'txn_id',
        'invoice_number',
        'invoice_date',
        'invoice_total',
        'shipping_amount',
        'supplies_amount',
        'quickbooks_vendor_name',
        'quickbooks_vendor_terms',
        'quickbooks_bank_account',
        'quickbooks_export_template',
        'status_code',
        'status_text',
        'deleted',
        'deleted_by',
        'exported',
        'exported_by',
    ]

    has_rows = True
    model_row_class = QuickbooksExportableInvoiceDistribution
    rows_filterable = False
    rows_pageable = False
    rows_viewable = False

    # TODO: this does not work right yet, e.g. clicking the View
    # action link will still trigger row-click event
    # clicking_row_checks_box = True

    row_labels = {
        'department_id': "Department ID",
        'status_code': "Status",
    }

    row_grid_columns = [
        'department_id',
        'department',
        'quickbooks_expense_account',
        'quickbooks_expense_class',
        'source_amount',
        'calculated_percent',
        'calculated_amount',
        'status_code',
    ]

    def configure_grid(self, g):
        super(ExportableInvoiceView, self).configure_grid(g)
        model = self.model

        # store
        g.set_joiner('store', lambda q: q.outerjoin(model.Store))
        g.set_filter('store', model.Store.name)
        g.set_sorter('store', model.Store.name)

        # vendor
        g.set_joiner('vendor', lambda q: q.outerjoin(model.Vendor))
        g.set_filter('vendor', model.Vendor.name)
        g.set_sorter('vendor', model.Vendor.name)
        g.set_link('vendor')

        # invoice_number
        g.filters['invoice_number'].default_active = True
        g.filters['invoice_number'].default_verb = 'contains'
        g.set_link('invoice_number')

        # invoice_date
        g.set_sort_defaults('invoice_date', 'desc')
        g.set_link('invoice_date')

        # currency fields
        g.set_type('invoice_total', 'currency')
        g.set_type('shipping_amount', 'currency')
        g.set_type('supplies_amount', 'currency')

        # status_code
        g.set_enum('status_code', model.QuickbooksExportableInvoice.STATUS)
        g.set_renderer('status_code', self.make_status_renderer(
            model.QuickbooksExportableInvoice.STATUS))

        # exported
        g.filters['exported'].default_active = True
        g.filters['exported'].default_verb = 'is_null'

        # deleted
        g.filters['deleted'].default_active = True
        g.filters['deleted'].default_verb = 'is_null'

        if self.has_perm('export'):
            g.checkboxes = True
            g.check_handler = 'rowChecked'
            g.check_all_handler = 'allChecked'

    def grid_extra_class(self, invoice, i):
        if invoice.deleted:
            return 'warning'
        if not self.exportable(invoice):
            if invoice.status_code in (invoice.STATUS_DEPTS_IGNORED,
                                       invoice.STATUS_EXPORTED,
                                       invoice.STATUS_DELETED):
                return 'notice'
            return 'warning'

    def checkbox(self, invoice):
        return self.exportable(invoice)

    def checked(self, invoice):
        return invoice.uuid in self.get_selected()

    def template_kwargs_index(self, **kwargs):
        kwargs = super(ExportableInvoiceView, self).template_kwargs_index(**kwargs)
        kwargs['selected'] = self.get_selected()
        return kwargs

    def get_selected(self):
        route_prefix = self.get_route_prefix()
        return self.request.session.get('{}.selected'.format(route_prefix), set())

    def set_selected(self, selected):
        route_prefix = self.get_route_prefix()
        self.request.session['{}.selected'.format(route_prefix)] = selected

    def exportable(self, invoice):
        """
        Return boolean indicating whether the given invoice is exportable.
        """
        return invoice.status_code == invoice.STATUS_EXPORTABLE

    def deletable_instance(self, invoice):
        if invoice.deleted:
            return False
        if invoice.exported:
            return False
        return True

    def delete_instance(self, invoice):
        app = self.get_rattail_app()
        session = app.get_session(invoice)
        invoice.deleted = app.make_utc()
        # nb. when bulk-deleting, user is in different session
        invoice.deleted_by = session.merge(self.request.user)
        invoice.status_code = invoice.STATUS_DELETED
        session.flush()

    def configure_form(self, f):
        super(ExportableInvoiceView, self).configure_form(f)
        model = self.model
        invoice = f.model_instance

        # store
        f.set_renderer('store', self.render_store)

        # vendor
        f.set_renderer('vendor', self.render_vendor)

        # currency fields
        f.set_type('invoice_total', 'currency')
        f.set_type('shipping_amount', 'currency')
        f.set_type('supplies_amount', 'currency')

        # status
        f.set_enum('status_code', model.QuickbooksExportableInvoice.STATUS)

        # exported
        if self.creating or not invoice.exported:
            f.remove('exported', 'exported_by')

        # deleted
        if self.creating or not invoice.deleted:
            f.remove('deleted', 'deleted_by')

    def get_row_data(self, invoice):
        model = self.model
        return self.Session.query(model.QuickbooksExportableInvoiceDistribution)\
                           .filter(model.QuickbooksExportableInvoiceDistribution.invoice == invoice)

    def get_parent(self, dist):
        return dist.invoice

    def configure_row_grid(self, g):
        super(ExportableInvoiceView, self).configure_row_grid(g)
        model = self.model

        # department_id
        g.set_sort_defaults('department_id')

        # amounts etc.
        g.set_type('source_amount', 'currency')
        g.set_type('calculated_percent', 'percent')
        g.set_type('calculated_amount', 'currency')

        # status
        g.set_renderer('status_code', self.make_status_renderer(
            model.QuickbooksExportableInvoiceDistribution.STATUS))

    def row_grid_extra_class(self, dist, i):
        if dist.status_code in (dist.STATUS_DEPT_IGNORED,
                                dist.STATUS_EXPORTED):
            return 'notice'
        elif dist.status_code != dist.STATUS_EXPORTABLE:
            return 'warning'

    def refresh(self):
        """
        View to refresh data for a single invoice.
        """
        invoice = self.get_instance()
        self.refresh_invoice(invoice)
        return self.redirect(self.get_action_url('view', invoice))

    def refresh_invoice(self, invoice, **kwargs):
        """
        Logic to actually refresh data for the given invoice.
        Implement as needed.
        """

    def refresh_results(self):
        """
        View to refresh data for all invoices in current search results.
        """
        # start thread to actually do work / report progress
        route_prefix = self.get_route_prefix()
        key = '{}.refresh_results'.format(route_prefix)
        progress = self.make_progress(key)
        results = self.get_effective_data()
        thread = Thread(target=self.refresh_results_thread,
                        args=(results, progress))
        thread.start()

        # show user the progress page
        return self.render_progress(progress, {
            'cancel_url': self.get_index_url(),
            'cancel_msg': "Refresh was canceled.",
        })

    def refresh_results_thread(self, results, progress):
        """
        Thread target, responsible for actually refreshing all
        invoices in the search results.
        """
        app = self.get_rattail_app()
        session = self.make_isolated_session()
        invoices = results.with_session(session).all()

        def refresh(invoice, i):
            self.refresh_invoice(invoice)

        try:
            app.progress_loop(refresh, invoices, progress,
                              message="Refreshing invoice data")

        except Exception as error:
            msg = "failed to refresh results!"
            log.warning(msg, exc_info=True)
            session.rollback()
            if progress:
                progress.session.load()
                progress.session['error'] = True
                progress.session['error_msg'] = "{}: {}".format(
                    msg, simple_error(error))
                progress.session.save()

        else:
            session.commit()
            if progress:
                progress.session.load()
                progress.session['complete'] = True
                progress.session['success_url'] = self.get_index_url()
                progress.session['success_msg'] = "Data refreshed for {} invoices".format(len(invoices))
                progress.session.save()

        finally:
            session.close()

    def select(self):
        """
        Mark one or more invoices as selected, within the current user's session.
        """
        model = self.model

        form = forms.Form(schema=ToggleInvoices(), request=self.request)
        if not form.validate():
            return {'error': "Form did not validate"}
        uuids = form.validated['uuids'].split(',')

        invoices = []
        for uuid in uuids:
            invoice = self.Session.get(model.QuickbooksExportableInvoice, uuid)
            if invoice and self.exportable(invoice):
                invoices.append(invoice)
        if not invoices:
            return {'error': "Must specify one or more valid invoice UUIDs."}

        selected = self.get_selected()
        for invoice in invoices:
            selected.add(invoice.uuid)
        self.set_selected(selected)
        return {
            'ok': True,
            'selected_count': len(selected),
        }

    def deselect(self):
        """
        Mark one or more invoices as *not* selected, within the current user's session.
        """
        model = self.model

        form = forms.Form(schema=ToggleInvoices(), request=self.request)
        if not form.validate():
            return {'error': "Form did not validate"}
        uuids = form.validated['uuids'].split(',')

        invoices = []
        for uuid in uuids:
            invoice = self.Session.get(model.QuickbooksExportableInvoice, uuid)
            if invoice and self.exportable(invoice):
                invoices.append(invoice)
        if not invoices:
            return {'error': "Must specify one or more valid invoice UUIDs."}

        selected = self.get_selected()
        for invoice in invoices:
            selected.discard(invoice.uuid)
        self.set_selected(selected)
        return {
            'ok': True,
            'selected_count': len(selected),
        }

    def export(self):
        """
        Export all currently-selected invoices.
        """
        model = self.model

        selected = self.get_selected()
        if not selected:
            self.request.session.flash("You must first select one or more "
                                       "invoices.", 'error')
            return self.redirect(self.get_index_url())

        invoices = []
        for uuid in selected:
            invoice = self.Session.get(model.QuickbooksExportableInvoice, uuid)
            if invoice and invoice.status_code == invoice.STATUS_EXPORTABLE:
                invoices.append(invoice)
            else:
                log.warning("invoice not found or wrong status: %s", uuid)

        if not invoices:
            self.request.session.flash("Hm, was unable to determine any invoices "
                                       "to export.", 'error')
            return self.redirect(self.get_index_url())

        # perform actual export and capture result
        try:
            result = self.do_export(invoices)

        except Exception as error:
            log.warning("failed to export invoices: %s",
                        [inv.uuid for inv in invoices],
                        exc_info=True)
            self.request.session.flash(simple_error(error), 'error')
            return self.redirect(self.request.get_referrer(
                default=self.get_index_url()))

        # clear out current checkbox selection
        self.set_selected(set())

        # result may be a redirect, e.g. to new export record.  if so
        # then just return as-is
        if isinstance(result, HTTPFound):
            return result

        # otherwise go back to invoice list
        return self.redirect(self.get_index_url())

    def do_export(self, invoices):
        export = self.make_invoice_export(invoices)
        self.update_export_status(invoices)
        url = self.request.route_url('quickbooks.invoice_exports.view',
                                     uuid=export.uuid)
        return self.redirect(url)

    def make_invoice_export_filename(self, invoices):
        raise NotImplementedError

    def make_invoice_export(self, invoices):
        model = self.model

        export = model.QuickbooksInvoiceExport()
        export.created_by = self.request.user
        export.record_count = len(invoices)
        export.filename = self.make_invoice_export_filename(invoices)
        self.Session.add(export)
        self.Session.flush()

        path = export.filepath(self.rattail_config, filename=export.filename,
                               makedirs=True)
        self.write_invoice_export_file(export, path, invoices)
        return export

    def write_invoice_export_file(self, export, path, invoices, progress=None):
        raise NotImplementedError

    def update_export_status(self, invoices):
        app = self.get_rattail_app()
        now = app.make_utc()
        for invoice in invoices:
            invoice.exported = now
            invoice.exported_by = self.request.user
            invoice.status_code = invoice.STATUS_EXPORTED
            for dist in invoice.distributions:
                if dist.status_code == dist.STATUS_EXPORTABLE:
                    dist.status_code = dist.STATUS_EXPORTED

    @classmethod
    def defaults(cls, config):
        cls._invoice_defaults(config)
        cls._defaults(config)

    @classmethod
    def _invoice_defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        url_prefix = cls.get_url_prefix()
        instance_url_prefix = cls.get_instance_url_prefix()
        permission_prefix = cls.get_permission_prefix()
        model_title_plural = cls.get_model_title_plural()

        # nb. must fix permission group title
        config.add_tailbone_permission_group(permission_prefix,
                                             model_title_plural, overwrite=False)

        # select
        config.add_route('{}.select'.format(route_prefix),
                         '{}/select'.format(url_prefix))
        config.add_view(cls, attr='select',
                        route_name='{}.select'.format(route_prefix),
                        request_method='POST',
                        permission='{}.export'.format(permission_prefix),
                        renderer='json')

        # deselect
        config.add_route('{}.deselect'.format(route_prefix),
                         '{}/deselect'.format(url_prefix))
        config.add_view(cls, attr='deselect',
                        route_name='{}.deselect'.format(route_prefix),
                        request_method='POST',
                        permission='{}.export'.format(permission_prefix),
                        renderer='json')

        # refresh invoice
        config.add_route('{}.refresh'.format(route_prefix),
                         '{}/refresh'.format(instance_url_prefix))
        config.add_view(cls, attr='refresh',
                        route_name='{}.refresh'.format(route_prefix),
                        request_method='POST',
                        permission='{}.export'.format(permission_prefix))

        # refresh results
        config.add_route('{}.refresh_results'.format(route_prefix),
                         '{}/refresh-results'.format(url_prefix))
        config.add_view(cls, attr='refresh_results',
                        route_name='{}.refresh_results'.format(route_prefix),
                        request_method='POST',
                        permission='{}.export'.format(permission_prefix))

        # export
        config.add_tailbone_permission(permission_prefix,
                                       '{}.export'.format(permission_prefix),
                                       "Export Invoices")
        config.add_route('{}.export'.format(route_prefix),
                         '{}/export'.format(url_prefix))
        config.add_view(cls, attr='export',
                        route_name='{}.export'.format(route_prefix),
                        request_method='POST',
                        permission='{}.export'.format(permission_prefix))


class InvoiceExportView(ExportMasterView):
    """
    Master view for Quickbooks invoice exports.
    """
    model_class = QuickbooksInvoiceExport
    route_prefix = 'quickbooks.invoice_exports'
    url_prefix = '/quickbooks/exports/invoice'
    downloadable = True
    delete_export_files = True

    grid_columns = [
        'id',
        'created',
        'created_by',
        'filename',
        'record_count',
    ]

    form_fields = [
        'id',
        'created',
        'created_by',
        'record_count',
        'filename',
    ]


def defaults(config, **kwargs):
    base = globals()

    ExportableInvoiceView = kwargs.get('ExportableInvoiceView', base['ExportableInvoiceView'])
    ExportableInvoiceView.defaults(config)

    InvoiceExportView = kwargs.get('InvoiceExportView', base['InvoiceExportView'])
    InvoiceExportView.defaults(config)


def includeme(config):
    defaults(config)
