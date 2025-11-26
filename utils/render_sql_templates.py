import jinja2

def render_sql_template(template_name, **kwargs):
    """
    Генерация SQL-запроса из Jinja темплейта
    """
    with open(template_name) as template_file:
        template = jinja2.Template(template_file.read())
    return template.render(**kwargs)