## -*- coding: utf-8; -*-

<%def name="render_xref_buttons()">
  <b-button type="is-primary"
            % if harvest_url:
            tag="a" href="${harvest_url}" target="_blank"
            % else:
            disabled title="${harvest_why_no_url}"
            % endif
            icon-pack="fas"
            icon-left="external-link-alt">
    View in Harvest
  </b-button>
</%def>

<%def name="render_xref_helper()">
  <nav class="panel">
    <p class="panel-heading">Cross-Reference</p>
    <div class="panel-block buttons">
      ${self.render_xref_buttons()}
    </div>
  </nav>
</%def>
