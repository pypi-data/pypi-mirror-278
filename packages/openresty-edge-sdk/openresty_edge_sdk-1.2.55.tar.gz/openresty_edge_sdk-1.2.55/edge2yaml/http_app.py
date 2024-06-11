import os

from .utils import error, warn, info, generate_certificates, \
    get_app_id_by_domain, fix_line, clear_changes, release_changes
from .read_config import read_yaml_file

def add_default_ssl_cert(client, app_id, domains, domain):
    rootCA_key, rootCA_crt, edge_node_key, edge_node_csr, edge_node_crt = generate_certificates(domains, domain)

    client.use_app(app_id)
    client.set_cert_key(cert=edge_node_crt, key=edge_node_key)

def add_http_app(client, partition_id, domains, cn_domain, access_log_name):
    domains_str = ",".join(domains)
    info(f"adding http application: {domains_str}, partition id: {partition_id}")
    access_log = dict()
    if access_log_name:
        access_log = {
            'filename': "access.log",
            'name': access_log_name,
        }
    http_ports = [80]
    https_ports = [443]
    partition_ids = [partition_id]

    try:
        label = f"app for partition {partition_id}"
        app_id = client.new_app(domains=domains, cluster_groups=partition_ids,
                                access_log=access_log, http_ports=http_ports,
                                https_ports=https_ports, label=label)
    except Exception as e:
        # just warning, do not interrupt the execution
        warn(f"failed to create app: {e}")

    try:
        info(f"adding ssl cert to app, app id: {app_id}, domain: {domains_str}")
        add_default_ssl_cert(client, app_id, domains, cn_domain)
    except Exception as e:
        # just warning, do not interrupt the execution
        warn(f"failed to ssl cert to app, app id: {app_id}, error: {e}")

    release_changes(client, app_id)
    return app_id

def process_http_app(client, partition_id, domain, configs_path):
    if not domain:
        error("missing argument: domain.")

    log_format = None
    app_config = None

    file = f"{configs_path}/app.yaml"
    if os.path.exists(file):
        app_config = read_yaml_file(file)

    if app_config and 'access_log_format' in app_config:
        # use the first domain
        log_format = app_config['access_log_format']

    domains = [domain]
    if app_config and 'domains' in app_config:
        app_domains = app_config['domains']
        for dn in app_domains:
            if dn != domain:
                domains.append(dn)

    # get app in partition
    app_id = get_app_id_by_domain(client, partition_id, domain)
    if app_id:
        client.use_app(app_id)

        need_release = False
        if log_format is not None:
            # if this configuration is not specified in the configuration file,
            # then we will not make changes
            data = client.get_app_config(app_id)
            cur_log_format = data.get('access_log', dict())
            cur_log_format_name = cur_log_format.get('name', None)
            if cur_log_format_name is None or cur_log_format_name != log_format:
                try:
                    info(f"updating app config, app id: {app_id}, file: app.yaml, line: {fix_line(app_config and app_config.lc.line or 0)}")
                    new_log_format = {'name': log_format, 'filename': 'access.log'}
                    client.put_app_config(app_id, access_log=new_log_format)
                    need_release = True
                except Exception as e:
                    clear_changes(client, app_id)
                    error(f"failed to update app config, app id: {app_id}, file: app.yaml, line: {fix_line(app_config and app_config.lc.line or 0)}, error: {e}")

        if app_config and 'domains' in app_config:
            # if this configuration is not specified in the configuration file,
            # then we will not make changes
            cur_domains = client.get_app_domains(app_id)
            cur_domains_map = dict()
            for dn in cur_domains:
                cur_domains_map[dn['domain']] = dn

            domain_changed = False
            for dn in domains:
                if dn not in cur_domains_map:
                    # new domain
                    domain_changed = True
                else:
                    del cur_domains_map[dn]

            if cur_domains_map:
                # domain has been removed
                domain_changed = True

            if domain_changed:
                try:
                    app = client.get_app()
                    info(f"updating app domains, app id: {app_id}, file: app.yaml, line: {fix_line(app_config and app_config.lc.line or 0)}")
                    client.put_app(app_id=app_id, domains=domains, label=app['name'])
                    need_release = True
                except Exception as e:
                    clear_changes(client, app_id)
                    error(f"failed to update app domains, app id: {app_id}, file: app.yaml, line: {fix_line(app_config and app_config.lc.line or 0)}, error: {e}")

        if need_release:
            release_changes(client, app_id)

        return app_id

    # app not found, create app
    return add_http_app(client, partition_id, domains, domain, log_format)

def cleanup_http_app(client, partition_id, domain):
    if not domain:
        warn("without specifying a domain name, the application will not be cleaned")

    # delete app
    app_id = get_app_id_by_domain(client, partition_id, domain)
    if app_id:
        info(f"removing app, app id: {app_id}")
        client.del_app(app_id)
