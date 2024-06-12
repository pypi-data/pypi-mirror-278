## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="render_form_buttons()">
  % if master.has_perm('export'):
      ${h.form(master.get_action_url('refresh', instance), **{'@submit': 'refreshingInvoice = true'})}
      ${h.csrf_token(request)}
      <b-button type="is-primary"
                native-type="submit"
                icon-pack="fas"
                icon-left="redo"
                :disabled="refreshingInvoice">
        {{ refreshingInvoice ? "Working, please wait..." : "Refresh Data" }}
      </b-button>
      ${h.end_form()}
  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ${form.component_studly}Data.refreshingInvoice = false

  </script>
</%def>


${parent.body()}
