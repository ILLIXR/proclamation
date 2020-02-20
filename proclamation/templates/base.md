{% macro format_ref(ref) -%}
    {%- if ref.item_type == "issue" -%}
        {%- set subdir = "issues" %}
        {%- set link_text %}#{{ ref.number }}{% endset %}
    {%- elif ref.item_type == "pr" -%}
        {%- set subdir = "pull" %}
        {%- set link_text %}#{{ ref.number }}{% endset %}
    {%- elif ref.item_type == "mr" -%}
        {%- set subdir = "merge_requests" %}
        {%- set link_text %}!{{ ref.number }}{% endset %}
    {%- endif -%}
[{{ link_text }}]({{base_url}}/{{subdir}}/{{ ref.number }})
{%- endmacro -%}
{% macro format_refs(refs) -%}
    {% if (refs | length) > 0 %} (
        {%- set comma = joiner(", ") -%}
        {% for ref in refs -%}
            {{comma()}}{{format_ref(ref)}}
        {%- endfor %})
    {%- endif %}
{%- endmacro -%}
{% block title %}## {{ project_name }} {{project_version}} ({{date}}){% endblock %}

{% for section in sections %}
- {{ section.name }}
{% for chunk in section.chunks %}
  - {{ (chunk.text + format_refs(chunk.refs)) | wordwrap | indent }}
{% else %}
  - No significant changes
{% endfor %}
{% endfor %}
