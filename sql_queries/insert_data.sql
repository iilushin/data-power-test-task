{%- set has_pk = columns.values() | selectattr("is_PK") | list | length > 0 %}

{%- if has_pk %}
INSERT OR IGNORE INTO {{ table_name }} (
{%- else %}
INSERT INTO {{ table_name }} (
{%- endif %}
    {{ columns.keys() | join(', ') }}
)
VALUES (
    {{ ("?," * (columns|length)).rstrip(",") }}
);
