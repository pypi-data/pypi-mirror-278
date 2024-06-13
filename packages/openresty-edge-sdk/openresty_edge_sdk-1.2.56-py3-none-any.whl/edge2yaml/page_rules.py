from .utils import error, warn, info, get_app_id_by_domain, fix_line, check_type, \
    get_md5_from_comment, cal_config_md5, clear_changes, release_changes
from .read_config import read_yaml_config
from .global_variables import replace_global_variable_in_el

def delete_page_rules(client, app_id):
    client.use_app(app_id)
    info(f"removing all page rules in app, app id: {app_id}")
    rules = client.get_all_rules(app_id)
    for rule in rules:
        if 'id' in rule:
            info(f"removing page rule from app, app id: {app_id}, page rule id: {rule['id']}")
            client.del_rule(rule['id'])

def check_page_rules(filename, rules):
    exp_rule = {
        'enable_rule': {
            'type': bool,
        },
        'actions': {
            'type': dict,
            'require': False,
        },
        'waf': {
            'type': dict,
            'require': False,
        },
        'cache': {
            'type': dict,
            'require': False,
        },
        'conditions': {
            'type': list,
            'require': False,
        },
        'order': {
            'type': int,
        },
        'comment': {
            'type': str,
        },
    }

    for rule in rules:
        for key, expected in exp_rule.items():
            if key not in rule:
                if expected.get('require', False):
                    error(f"missing key \"{key}\" in rule, filename: {filename}, line: {fix_line(rule.lc.line)}")
                else:
                    continue

            expected_type = expected['type']
            if not check_type(rule[key], expected_type):
                error(f"incorrect type for key: {key}, expected {expected_type}, got {type(rule[key])}, filename: {filename}, line: {fix_line(rule.lc.line)}")

    return True

def process_page_rules(client, app_id, partition_id, location, configs_path):
    # read local rules
    configs = read_yaml_config(configs_path, location)
    if not configs:
        error("no page rules were found in the local page rules file. if you want to delete page rules from Edge Admin, please use the cleanup option.")

    info("checking if page rules have changed")

    client.use_app(app_id)

    sorted_filenames = sorted(configs.keys())

    # check local rules
    for filename in sorted_filenames:
        config = configs[filename]
        check_page_rules(filename, config)

    # read remote rules
    old_rules = client.get_all_rules(app_id)
    old_rules_md5 = dict()
    old_orders = list()
    for rule in old_rules:
        if 'comment' in rule:
            md5 = get_md5_from_comment(rule['comment'])
            if md5:
                if md5 not in old_rules_md5:
                    old_rules_md5[md5] = list()

                old_rules_md5[md5].append(rule['id'])

        old_orders.append(rule['id'])

    # add local rules to admin
    order = 0
    new_orders = list()
    keep_old_ids = dict()
    for filename in sorted_filenames:
        rules = configs[filename]
        for rule in rules:
            order = order + 1
            md5 = cal_config_md5(rule)
            if md5 in old_rules_md5 and len(old_rules_md5[md5]) > 0:
                # rule have not changed
                first_id = old_rules_md5[md5][0]
                del old_rules_md5[md5][0]   # remove from list
                new_orders.append(first_id)
                keep_old_ids[first_id] = True
                continue

            # changed
            conditions = rule.get('conditions', None)
            actions = rule.get('actions', None)
            enable_rule = rule.get('enable_rule', True)
            cache = rule.get('cache', None)
            waf = rule.get('waf', None)
            proxy = rule.get('proxy', None)
            comment = rule.get('comment', None)

            replace_global_variable_in_el(client, actions, filename, partition_id)

            if comment:
                comment = get_real_comment(comment)
                comment = f"{comment}\nmd5: {md5}, please do not modify."
            else:
                comment = f"md5: {md5}, please do not modify."

            try:
                info(f"adding page rule to app, app id: {app_id}, file: {filename}, line: {fix_line(rule.lc.line)}")
                rule_id = client.new_rule(condition=conditions, conseq=actions,
                                        order=order, enable=enable_rule,
                                        comment=comment, waf=waf, proxy=proxy,
                                        cache=cache)

                new_orders.append(rule_id)
            except Exception as e:
                clear_changes(client, app_id)
                error(f"failed to add page rule to app, app id: {app_id}, file: {filename}, line: {fix_line(rule.lc.line)}", e)

    # remove rules no longer needed
    for rule in old_rules:
        if rule['id'] in keep_old_ids:
            continue

        try:
            # no longer needed
            info(f"removing page rule from app, app id: {app_id}, page rule id: {rule['id']}")
            client.del_rule(rule['id'])
        except Exception as e:
            clear_changes(client, app_id)
            error(f"failed to remove page rule from app, app id: {app_id}, rule id: {rule['id']}", e)

    # check if need to reorder
    if old_orders != new_orders:
        order = 1
        orders = dict()
        for rule_id in new_orders:
            orders[rule_id] = order
            order = order + 1

        if orders:
            try:
                info(f"reordering the page rules, app id: {app_id}")
                client.reorder_rules(orders)
            except Exception as e:
                clear_changes(client, app_id)
                error(f"failed to reorder page rule, app id: {app_id}", e)

    release_changes(client, app_id)


def cleanup_page_rules(client, partition_id, domain):
    app_id = get_app_id_by_domain(client, partition_id, domain)
    if not app_id:
        error(f"app not found, app id: {app_id}, domain: {domain}")

    delete_page_rules(client, app_id)
    release_changes(client, app_id)
