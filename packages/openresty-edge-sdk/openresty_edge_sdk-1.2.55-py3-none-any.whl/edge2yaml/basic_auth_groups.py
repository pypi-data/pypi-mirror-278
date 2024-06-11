from .utils import error, warn, info, get_md5_from_comment, cal_config_md5, fix_line
from .read_config import read_yaml_config

def check_basic_auth_groups(group, filename):
    if not isinstance(group, dict):
        error("unsupported file format for basic auth groups, file: {filename}")

    if 'name' not in group:
        error("basic auth group name not found, file: {filename}")

    if 'users' not in group:
        error("basic auth group users not found, file: {filename}")

    label = group.get('label', '')
    group_name = group['name']
    if not isinstance(label, str):
        error(f"basic auth group label must be a string, file: {filename}, line: {fix_line(label.lc.line)}")

    users = group['users']
    for user in users:
        username = user.get("username", None)
        password = user.get("password", None)

        if not isinstance(username, str):
            error(f"invalid username in basic auth group {group_name}: {username}, file: {filename}, line: {fix_line(user.lc.line)}")

        if not isinstance(password, str):
            error(f"invalid password in basic auth group {group_name}: {password}, file: {filename}, line: {fix_line(user.lc.line)}")

    return True

def update_basic_auth_users(client, app_id, group_id, users):
    # get all users
    old_users = client.get_app_basic_auth_users_in_group(group_id, app_id=app_id)

    old_users_map = dict()
    for u in old_users:
        old_users_map[u['username']] = u

    for user in users:
        username = user['username']
        password = user['password']

        if username in old_users_map:
            # update
            try:
                info(f"updating basic auth user \"{username}\" to group, app id: {app_id}, group id: {group_id}")
                user_id = old_users_map[username]['id']
                client.put_app_basic_auth_user(user_id, group_id, username, password, app_id=app_id)
            except Exception as e:
                error(f"failed to update basic auth user, file: {filename}, line: {fix_line(user.lc.line)}", e)

            del(old_users_map[username])
        else:
            # add
            try:
                info(f"adding basic auth user \"{username}\" to group, app id: {app_id}, group id: {group_id}")
                client.new_app_basic_auth_user(group_id, username, password, app_id=app_id)
            except Exception as e:
                error(f"failed to add basic auth user, file: {filename}, line: {fix_line(user.lc.line)}", e)
            pass

    # delete
    for username, user in old_users_map.items():
        try:
            info(f"deleting basic auth user \"{username}\" from group, app id: {app_id}, group id: {group_id}")
            client.del_app_basic_auth_user(user["id"], group_id, app_id=app_id)
        except Exception as e:
            error(f"failed to delete basic auth user, file: {filename}, line: {fix_line(user.lc.line)}", e)


def basic_auth_group_changed(old_group, new_md5):
    if 'label' not in old_group:
        return True

    old_md5 = get_md5_from_comment(old_group['label'])
    if new_md5 and old_md5 == new_md5:
        return False

    return True

def process_basic_auth_groups(client, app_id, location, configs_path):
    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    # pre check
    info("checking if basic auth groups are valid")
    for filename, group in configs.items():
        check_basic_auth_groups(group, filename)

    info("checking if basic auth groups have changed")
    old_groups = client.get_all_app_basic_auth_user_groups(app_id)
    old_groups_map = dict()

    for g in old_groups:
        old_groups_map[g['name']] = g

    for filename, new_group in configs.items():
        # check if group exists
        name = new_group['name']
        md5 = cal_config_md5(new_group)

        if name not in old_groups_map:
            try:
                info(f"adding basic auth group \"{name}\" to app, app id: {app_id}")
                label = f"md5: {md5}, please do not modify."
                group_id = client.new_app_basic_auth_user_group(name, label=label, app_id=app_id)
                update_basic_auth_users(client, app_id, group_id, new_group['users'])
            except Exception as e:
                error(f"failed to add basic auth group to app, file: {filename}, line: {fix_line(new_group.lc.line)}", e)

            # process next
            continue

        # group exists, check if group changed
        if basic_auth_group_changed(old_groups_map[name], md5):
            label = old_groups_map[name]['label']
            if label:
                label = get_real_comment(label)
                label = f"{label}md5: {md5}, please do not modify."
            else:
                label = f"md5: {md5}, please do not modify."

            try:
                group_id = old_groups_map[name]['id']
                update_basic_auth_users(client, app_id, group_id, new_group['users'])
                info(f"updating basic auth group \"{name}\" to app, app id: {app_id}")
                client.put_app_basic_auth_user_group(group_id, name, label=label, app_id=app_id)
            except Exception as e:
                error(f"failed to update basic auth group to app, file: {filename}, line: {fix_line(new_group.lc.line)}", e)

        del(old_groups_map[name])

    # delete
    for name, group in old_groups_map.items():
        try:
            info(f"deleting basic auth group \"{name}\" from app, app id: {app_id}")
            client.del_app_basic_auth_user_group(group["id"], app_id=app_id)
        except Exception as e:
            error(f"failed to delete basic auth group to app, group id: {group['id']}, app id {app_id}", e)
