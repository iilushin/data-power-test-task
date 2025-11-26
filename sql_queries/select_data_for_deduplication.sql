SELECT
    {{ columns | join(', ') }}
FROM {{ table_name }}
