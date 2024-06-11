## -*- coding: utf-8; mode: conf; -*-
<%inherit file="rattail.projects:rattail_adjacent/package/templates/installer/rattail.conf.mako" />
${parent.body()}

####################
## preamble
####################

<%def name="render_group_preamble()">
${parent.render_group_preamble()}

[corepos]
foo = bar
</%def>
