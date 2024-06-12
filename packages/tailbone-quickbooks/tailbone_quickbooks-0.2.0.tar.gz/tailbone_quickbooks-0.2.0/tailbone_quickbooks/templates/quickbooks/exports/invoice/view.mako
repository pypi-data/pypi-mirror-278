## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="context_menu_items()">
  % if request.has_perm('quickbooks.exportable_invoices.list'):
      <li>${h.link_to("Back to Exportable Invoices", url('quickbooks.exportable_invoices'))}</li>
  % endif
</%def>


${parent.body()}
