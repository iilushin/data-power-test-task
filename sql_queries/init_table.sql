CREATE TABLE IF NOT EXISTS {{ table_name }} (
{%- for col, props in columns.items() %}
    {{ col }} {{ props.data_type }}{% if props.is_PK %} PRIMARY KEY{% endif %}{% if not props.is_nullable %} NOT NULL{% endif %}{% if not loop.last %},{% endif %}
{%- endfor %}
);
