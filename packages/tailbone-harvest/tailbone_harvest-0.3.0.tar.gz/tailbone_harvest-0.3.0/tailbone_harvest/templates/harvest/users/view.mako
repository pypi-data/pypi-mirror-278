## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="page_content()">

  % if instance.avatar_url:
      <div style="margin: 1rem;">
        <img src="${instance.avatar_url}" />
      </div>
  % endif

  ${parent.page_content()}
</%def>


${parent.body()}
