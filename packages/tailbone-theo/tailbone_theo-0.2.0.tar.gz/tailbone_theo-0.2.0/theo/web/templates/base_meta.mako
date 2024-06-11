## -*- coding: utf-8; mode: html; -*-
<%inherit file="tailbone:templates/base_meta.mako" />

<%def name="footer()">
  <p class="has-text-centered">
    ${h.link_to("Theo {}{}".format(theo.__version__, '' if request.rattail_config.production() else '+dev'), url('about'))}
  </p>
  % if request.rattail_config.getbool('theo', 'link_to_mobile', default=False):
      <p class="has-text-centered">
        ${h.link_to("View Mobile App", '/m/')}
      </p>
  % endif
</%def>
