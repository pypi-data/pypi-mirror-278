import re

from .utils import error, warn, info, gen_var_name, fix_line

def replace_global_variable(client, content, content_type, partition_id):
    if not isinstance(content, str):
        raise Exception("bad content")

    variables = []
    pattern = r'\$or_global_user_variable_[a-zA-Z0-9_]+'
    variables = re.findall(pattern, content)

    variable_names = {}
    for var in variables:
        match = re.search(r'\$or_global_user_variable_(.*)', var)
        # should always match
        name = match.group(1)
        var_name = gen_var_name(name, partition_id)
        variable_names[var] = var_name

    global_variables = client.get_all_global_vars()
    if not isinstance(global_variables, list):
        global_variables = list()

    global_variable_names = {}
    for var in global_variables:
        global_variable_names[var['name']] = var['id']

    for fake_name, real_name in variable_names.items():
        if real_name not in global_variable_names:
            raise Exception(f"global variable not found in Edge Admin: {real_name}")

        var_id = global_variable_names[real_name]

        # print(f"replacing {fake_name} to $or-global-{var_id}")
        content = content.replace(fake_name, f'$or-global-{var_id}')

    return content

def replace_global_variable_in_el(client, actions, filename, partition_id):
    if not isinstance(actions, dict) or 'user-code' not in actions:
        return

    el_value = ''
    user_code_data = actions['user-code']
    if isinstance(user_code_data, dict) and 'el' in user_code_data:
        el_value = user_code_data['el']
    else:
        if user_code_data:
            error(f"bad actions in page rule, file: {filename}, line: {fix_line(user_code_data.lc.line)}")
        else:
            error(f"bad actions in page rule, file: {filename}, line: {fix_line(actions.lc.line)}")

    try:
        user_code_data['el'] = replace_global_variable(client, el_value, "Edgelang", partition_id)
    except Exception as e:
        error(f"failed to replace global variable in Edgelang, file: {filename}, line: {fix_line(el_value.lc.line)}", e)

def replace_global_variable_in_log_formats(client, log_formats, filename, partition_id):
    for name, fmt in log_formats.items():
        try:
            log_format = fmt['format']
            fmt['format'] = replace_global_variable(client, log_format, "access log format", partition_id)
        except Exception as e:
            error(f"failed to replace global variable in access log format, file: {filename}, log format: {name}", e)
