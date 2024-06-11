## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="object_helpers()">
  ${parent.object_helpers()}
  ${self.render_import_helper()}
</%def>

<%def name="render_import_helper()">
  % if master.has_perm('import_from_harvest'):
      <nav class="panel">
        <p class="panel-heading">Re-Import</p>
        <div class="panel-block buttons">
          <div style="display: flex; flex-direction: column;">
            % if master.has_perm('import_from_harvest'):
                ${h.form(master.get_action_url('import_from_harvest', instance), **{'@submit': 'importFromHarvestSubmitting = true'})}
                ${h.csrf_token(request)}
                <b-button type="is-primary"
                          native-type="submit"
                          icon-pack="fas"
                          icon-left="redo"
                          :disabled="importFromHarvestSubmitting">
                  {{ importFromHarvestSubmitting ? "Working, please wait..." : "Re-Import from Harvest" }}
                </b-button>
                ${h.end_form()}
            % endif
          </div>
        </div>
      </nav>
  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  % if master.has_perm('import_from_harvest'):
      <script type="text/javascript">

        ThisPageData.importFromHarvestSubmitting = false

      </script>
  % endif
</%def>


${parent.body()}
