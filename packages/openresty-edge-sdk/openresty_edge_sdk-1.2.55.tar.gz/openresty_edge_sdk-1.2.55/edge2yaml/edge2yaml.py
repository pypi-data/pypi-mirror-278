# -*- coding: utf-8 -*-

import warnings
import os
import sys
import hashlib
import requests
import argparse
import urllib3
import datetime
import traceback
import socket
from edge2client import Edge2Client
from .utils import error, warn, info, md5sum, cal_config_md5, gen_var_name, \
    release_changes, clear_changes, release_partition_changes, \
    clear_partition_changes, fix_line
from .http_app import process_http_app, cleanup_http_app
from .read_config import read_yaml_config
from .global_configs import cleanup_global_configs, process_global_configs
from .upstreams import process_upstreams, cleanup_app_upstreams
from .page_rules import process_page_rules, cleanup_page_rules
from .global_lua_modules import cleanup_global_lua_modules, process_global_lua_modules
from .basic_auth_groups import process_basic_auth_groups
from .users import process_users
from .edge_email import read_email_configs

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

supported_locations = {
    'page_rules': True,
    'upstreams': True,
    'global_lua_modules': True,
    'global_configs': True,
    'basic_auth_groups': True,
    'users': True,
}

def parse_args():
    description = "Update or add OpenResty Edge configuration."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--api-token", dest="api_token", action="store", required=True,
                        help="specify the API Token for sending the request")
    parser.add_argument("-u", "--admin-url", dest="admin_url", action="store", required=True,
                        help="specify the URL of the OpenResty Edge Admin. For example, https://admin.com:443")
    parser.add_argument("-s", "--disable-ssl-verify", dest="disable_ssl_verify", action="store_true", default=False,
                        help="turn off SSL verify for requests to access OpenResty Edge Admin")
    parser.add_argument("-c", "--cleanup", dest="cleanup", action="store_true", default=False,
                        help="based on the location. This option allows for the cleanup of page rules, application upstreams, global user variables, and resetting the access log format for partitions. It can also be used independently of the location")
    parser.add_argument("-i", "--configs-path", dest="configs_path", action="store", required=True,
                        help="specify the path to the configuration file")
    parser.add_argument("-e", "--email-config-file", dest="email_config_file", action="store", required=False,
                        help="specify the file to the email configuration; if not specified, the email.yaml file in the configuration path will be used")
    parser.add_argument("-U", "--users-config-path", dest="users_config_path", action="store", required=False,
                        help="specify the path to the users configuration; if not specified, the users/ path in the configuration path will be used")

    keys_string = ', '.join(supported_locations.keys())
    parser.add_argument("-l", "--location", dest="location", action="store",
                        help=f"specify the configuration name that needs to be updated, supported: {keys_string}")
    parser.add_argument("-d", "--domain", dest="domain", action="store",
                        help="specify a domain name. When an HTTP application containing this domain exists, it will be updated; otherwise, a new application will be created")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--partition-id", dest="partition_id", action="store", type=int,
                        help="specify the id of the partition where you want to add or update the configuration")
    group.add_argument("-n", "--partition-name", dest="partition_name", action="store",
                        help="specify the name of the partition where you want to add or update the configuration")

    args = parser.parse_args()

    return args

def cleanup(client, partition_id, domain, location):
    if location == "page_rules":
        cleanup_page_rules(client, partition_id, domain)

    elif location == "upstreams":
        cleanup_app_upstreams(client, partition_id, domain)

    elif location == "global_lua_modules":
        cleanup_global_lua_modules(client, partition_id)

    elif location == "global_configs":
        cleanup_global_configs(client, partition_id)

    else:
        cleanup_http_app(client, partition_id, domain)
        cleanup_global_configs(client, partition_id)
        cleanup_global_lua_modules(client, partition_id)

def check_partition(client, partition_id, partition_name):
    if partition_id:
        data = client.get_cluster_group(partition_id)
        if not data:
            error(f'partition not found, partition id: {partition_id}')

        return partition_id

    if partition_name:
        partitions = client.get_all_cluster_groups()
        for p in partitions:
            if p['name'] == partition_name:
                # get partition_id
                return p['id']

        error(f'partition not found, partition name: {partition_name}')

def main(args=None):
    args = parse_args()

    ssl_verify = True
    if args.disable_ssl_verify is True:
        ssl_verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings()

    location = args.location
    if location is not None and location not in supported_locations:
        error(f"unsupported location: {location}")

    configs_path = args.configs_path
    if not configs_path or not os.path.exists(configs_path) or not os.path.isdir(configs_path):
        error(f"bad configs path: {configs_path}")

    email_config_file = args.email_config_file
    if email_config_file and not os.path.exists(email_config_file):
        error(f"email config file not found: {email_config_file}")

    if not email_config_file:
        email_config_file = f"{configs_path}/email.yaml"

    users_config_path = args.users_config_path
    if users_config_path and not os.path.exists(users_config_path):
        error(f"users config path not found: {users_config_path}")

    if not users_config_path:
        users_config_path = f"{configs_path}/users"

    email_config = read_email_configs(email_config_file)

    client = Edge2Client(args.admin_url, None, None, args.api_token)
    client.set_ssl_verify(ssl_verify)

    partition_id = args.partition_id
    partition_name = args.partition_name
    partition_id = check_partition(client, partition_id, partition_name)

    domain = args.domain
    if not domain:
        error("no domain specified")

    if args.cleanup:
        cleanup(client, partition_id, domain, location)
        print("[!] Cleanup Finished.")
        sys.exit()

    if location == "page_rules":
        app_id = process_http_app(client, partition_id, domain, configs_path)
        process_page_rules(client, app_id, partition_id, location, configs_path)
    elif location == "upstreams":
        app_id = process_http_app(client, partition_id, domain, configs_path)
        process_upstreams(client, app_id, location, configs_path)
    elif location == "global_lua_modules":
        process_global_lua_modules(client, partition_id, location, configs_path)
    elif location == "global_configs":
        process_global_configs(client, partition_id, location, configs_path)
    elif location == "basic_auth_groups":
        app_id = process_http_app(client, partition_id, domain, configs_path)
        process_basic_auth_groups(client, app_id, location, configs_path)
    elif location == "users":
        process_users(client, users_config_path, email_config)
    else:
        process_global_configs(client, partition_id, "global_configs", configs_path)
        process_global_lua_modules(client, partition_id, "global_lua_modules", configs_path)
        app_id = process_http_app(client, partition_id, domain, configs_path)
        # TODO add/update before updating page rules, delete after page rules
        process_upstreams(client, app_id, "upstreams", configs_path)
        process_basic_auth_groups(client, app_id, "basic_auth_groups", configs_path)
        process_page_rules(client, app_id, partition_id, "page_rules", configs_path)
        process_users(client, users_config_path, email_config)

    print("[!] Finished.")

if __name__ == "__main__":
    exit(main())
