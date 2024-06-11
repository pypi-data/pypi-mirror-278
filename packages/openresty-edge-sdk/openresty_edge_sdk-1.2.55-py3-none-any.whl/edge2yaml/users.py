from jinja2 import Template

from .utils import error, warn, info, fix_line
from .read_config import read_yaml_config
from .edge_email import send_email

login_types = {
    'Normal': 'normal',
    'LDAP': 'ldap',
    'OpenIDC': 'oidc',
    'none': 'none',
}

def render_email(template, username, password, user_id, user_group, user_group_id):
    tm = Template(template)
    return tm.render(username=username, password=password,
                     user_id=user_id, user_group=user_group,
                     user_group_id=user_group_id)

def send_email_to_user(email_configs, user, user_id, group, user_groups):
    subject = email_configs['new_user_email_template']['subject']
    content = email_configs['new_user_email_template']['content']
    content = render_email(content, user['username'], user['password'],
                            user_id, group, user_groups[group])
    info("sending email to user: " + user['username'] + ", email: " + user['email'])
    ok = send_email(email_configs, user['email'], subject, content)
    if not ok:
        error("send email to " + user['email'] + " failed")

def process_users(client, configs_path, email_configs):
    configs = read_yaml_config(configs_path)
    if configs is None:
        return True

    users = list()
    user_groups = None
    sorted_filenames = sorted(configs.keys())
    # check users and format users
    for filename in sorted_filenames:
        config = configs[filename]
        if not isinstance(config, dict):
            error(f"unsupported file format for users, file: {filename}")

        if 'users' not in config:
            error(f"users not found in file: {filename}")

        def_change_pwd_on_login = config.get('change_pwd_on_login', False)
        def_login_type = config.get('login_type', 'Normal')
        def_password = config.get('password', None)
        def_allow_login = config.get('allow_login', True)
        def_group = config.get('group', None)
        def_send_email_to_existing_user = config.get('send_email_to_existing_user', False)
        def_send_email_to_new_user = config.get('send_email_to_new_user', False)

        for user in config['users']:
            if not isinstance(user, dict):
                error(f"unsupported file format for users, file: {filename}, line: {fix_line(user.lc.line)}")

            if 'username' not in user:
                error(f"username not found in user, file: {filename}, line: {fix_line(user.lc.line)}")

            login_type = user.get('login_type', def_login_type)
            if login_type is None:
                error(f"login type not found in user, file: {filename}, line: {fix_line(user.lc.line)}")

            if login_type not in login_types:
                error(f"unsupported login type: {login_type}, file: {filename}, line: {fix_line(user.lc.line)}")

            password = user.get('password', def_password)
            if not isinstance(password, str):
                error(f"password must be a string, file: {filename}, line: {fix_line(user.lc.line)}")

            allow_login = user.get('allow_login', def_allow_login)
            if not isinstance(allow_login, bool):
                error(f"allow_login must be a boolean, file: {filename}, line: {fix_line(user.lc.line)}")

            if allow_login is False:
                login_type = 'none'

            change_pwd_on_login = user.get('change_pwd_on_login', def_change_pwd_on_login)
            if not isinstance(change_pwd_on_login, bool):
                error(f"change_pwd_on_login must be a boolean, file: {filename}, line: {fix_line(user.lc.line)}")

            group = user.get('group', def_group)
            if not isinstance(group, str):
                error(f"group must be a string, file: {filename}, line: {fix_line(user.lc.line)}")

            # check if user group exists
            if user_groups is None:
                groups = client.get_all_user_groups()
                if groups is None:
                    error(f"failed to get user groups")

                user_groups = dict()
                for g in groups:
                    # g['permission'] = None
                    name = g['label']
                    user_groups[name] = g['id']

            if group not in user_groups:
                error(f"group not found: {group}, file: {filename}, line: {fix_line(user.lc.line)}")

            if 'email' not in user and user.get('send_email_to_new_user', False) == True:
                error(f"email not found in user, file: {filename}, line: {fix_line(user.lc.line)}")

            users.append({
                'username': user['username'],
                'password': password,
                'requires_password_change': change_pwd_on_login,
                # TODO support multiple login_types and groups
                'login_type': [ login_types[login_type] ],
                'gid': [ user_groups[group] ],
                'email': user.get('email', None),
                'send_email_to_existing_user': user.get('send_email_to_existing_user', def_send_email_to_existing_user),
                'send_email_to_new_user': user.get('send_email_to_new_user', def_send_email_to_new_user),
            })

    for user in users:
        # check if user exists
        data = client.search_global_user(user['username'])
        user_id = data.get('id', None)

        if isinstance(user_id, int):
            # check next users
            warn(f"user {user['username']} already exists, id: {user_id}")

            if 'email' in user and user.get('send_email_to_existing_user', None) == True:
                send_email_to_user(email_configs, user, user_id, group, user_groups)

            continue

        # new user
        data = client.add_global_user(user['username'], user['password'],
                               gid=user['gid'],
                               login_type=user['login_type'],
                               requires_password_change=user['requires_password_change'])

        user_id = data.get('id', None)
        if not isinstance(user_id, int):
            error(f"failed to add user: {user['username']}")

        info("added user: " + user['username'] + ", id: " + str(user_id) + ", user group: " + str(group))

        # send email
        if 'email' in user and user.get('send_email_to_new_user', False) == True:
            send_email_to_user(email_configs, user, user_id, group, user_groups)
