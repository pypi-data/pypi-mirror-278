import hashlib
import sys
import traceback
import ipaddress
import json
import re

def error(msg, e=None):
    if e:
        stack_trace = traceback.format_exc()
        sys.exit(f'[!] Error: {msg}, detail: {stack_trace}.')
    else:
        sys.exit(f'[!] Error: {msg}.')

def warn(msg):
    print(f'[?] Warn: {msg}.')

def info(msg):
    print(f'[+] Info: {msg}.')

def md5sum(string_to_hash):
    hash_object = hashlib.md5()
    hash_object.update(string_to_hash.encode('utf-8'))
    md5_hash = hash_object.hexdigest()
    return md5_hash

def cal_config_md5(config):
    json_str = json.dumps(config, ensure_ascii=False, sort_keys=True)
    return md5sum(json_str)

def gen_var_name(name, partition_id):
    return f"{name}_for_partition_{partition_id}"

import os
from OpenSSL import crypto

def generate_certificates(domains, domain):
    # 1. Generate the CA Root certificate and key
    ca_key = crypto.PKey()
    ca_key.generate_key(crypto.TYPE_RSA, 4096)

    ca_cert = crypto.X509()
    ca_cert.set_version(2)
    ca_cert.set_serial_number(1)
    ca_subject = ca_cert.get_subject()
    ca_subject.CN = f"{domain}.ca"
    ca_subject.C = "US"
    ca_subject.L = "San Fransisco"
    ca_cert.set_issuer(ca_subject)
    ca_cert.set_pubkey(ca_key)
    ca_cert.gmtime_adj_notBefore(0)
    ca_cert.gmtime_adj_notAfter(3650 * 24 * 60 * 60)
    ca_cert.sign(ca_key, "sha256")

    rootCA_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key)
    rootCA_crt = crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert)

    # 2. Generate the server private key
    server_key = crypto.PKey()
    server_key.generate_key(crypto.TYPE_RSA, 2048)
    edge_node_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, server_key)

    # 3. Create the certificate signing request (csr)
    server_csr = crypto.X509Req()
    server_subject = server_csr.get_subject()
    server_subject.C = "US"
    server_subject.ST = "CA"
    server_subject.O = "Organization, Inc."
    server_subject.CN = f"{domain}"

    excluded_values = [ domain ]
    # Add Subject Alternative Names (SAN) for additional domains
    san_list = [f"DNS:{dn}" for dn in domains if dn not in excluded_values]
    if san_list:
        san_ext = crypto.X509Extension(b"subjectAltName", False, ", ".join(san_list).encode())
        server_csr.add_extensions([san_ext])

    server_csr.set_pubkey(server_key)
    server_csr.sign(server_key, "sha256")
    edge_node_csr = crypto.dump_certificate_request(crypto.FILETYPE_PEM, server_csr)

    # 4. Generate the certificate using the csr and key along with the CA Root key
    server_cert = crypto.X509()
    server_cert.set_serial_number(1)
    server_cert.gmtime_adj_notBefore(0)
    server_cert.gmtime_adj_notAfter(3650 * 24 * 60 * 60)
    server_cert.set_issuer(ca_cert.get_subject())
    server_cert.set_subject(server_csr.get_subject())
    server_cert.set_pubkey(server_csr.get_pubkey())
    if san_list:
        server_cert.add_extensions(server_csr.get_extensions())
    server_cert.sign(ca_key, "sha256")
    edge_node_crt = crypto.dump_certificate(crypto.FILETYPE_PEM, server_cert)

    rootCA_key = rootCA_key.decode('utf-8')
    rootCA_crt = rootCA_crt.decode('utf-8')
    edge_node_key = edge_node_key.decode('utf-8')
    edge_node_csr = edge_node_csr.decode('utf-8')
    edge_node_crt = edge_node_crt.decode('utf-8')

    return rootCA_key, rootCA_crt, edge_node_key, edge_node_csr, edge_node_crt

def release_changes(client, app_id):
    if client.pending_changes(app_id=app_id) > 0:
        info(f"releasing pending changes of app id: {app_id}")
        client.new_release(app_id=app_id)

def clear_changes(client, app_id):
    if client.pending_changes(app_id=app_id) > 0:
        info(f"clearing pending changes of app id: {app_id}")
        client.clear_pending_changes(app_id=app_id)

def release_partition_changes(client, partition_id):
    try:
        count = client.pending_changes(app_type="partition", app_id=partition_id)
        if count > 0:
            info(f"releasing pending changes of partition id: {partition_id}")
            client.new_release(app_type="partition", app_id=partition_id)
    except Exception as e:
        warn(f"releasing pending changes of partition failed, partition id: {partition_id}, error: {e}")
        return

def clear_partition_changes(client, partition_id):
    try:
        count = client.pending_changes(app_type="partition", app_id=partition_id)
        if count > 0:
            info(f"clearing pending changes of partition id: {partition_id}")
            client.clear_pending_changes(app_type="partition", app_id=partition_id)
    except Exception as e:
        warn(f"clearing pending changes of partition failed, partition id: {partition_id}, error: {e}")
        return

def fix_line(line):
    if isinstance(line, int):
        return line + 1
    return None

def check_type(value, expected_type):
    if isinstance(value, expected_type):
        return True
    return False

def get_real_comment(comment):
    if not comment:
        return ''

    pattern = r"md5: [a-f0-9A-F]+, please do not modify\."
    comment = re.sub(pattern, "", comment)
    return comment.strip()

def get_md5_from_comment(comment):
    if not comment:
        return None

    match = re.search(r'md5: ([a-f0-9A-F]+), please do not modify\.', comment)
    if match:
        return match.group(1)

    return None

def get_updated_list(new_dict, old_list, major_key, compare_keys, changed_only=False):
    # check if config changed
    need_update = False
    updated_list = list()
    for old_config in old_list:
        if major_key in old_config and old_config[major_key] in new_dict:
            major = old_config[major_key]
            new_config = new_dict[major]
            for compare_key in compare_keys:
                old_val = old_config.get(compare_key, None)
                new_val = new_config.get(compare_key, None)
                if old_val != new_val:
                    old_config[compare_key] = new_val
                    need_update = True
                    if changed_only:
                        updated_list.append(old_config)

            new_dict[major] = None

        if not changed_only:
            updated_list.append(old_config)

    # new format
    for key, new_config in new_dict.items():
        if new_config is not None:
            updated_list.append(new_config)
            need_update = True

    if need_update:
        return updated_list

    return None

def is_valid_ipv4_address(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def is_valid_ipv6_address(address):
    try:
        ipaddress.IPv6Address(address)
        return True
    except ValueError:
        return False

def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[-A-Z0-9]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def is_valid_host(host):
    return is_valid_ipv4_address(host) or is_valid_ipv6_address(host) or is_valid_hostname(host)

def get_app_id_by_domain(client, partition_id, domain):
    uri = f"applications?detail=1&type=http&partition_id={partition_id}"
    apps = client.get_all(uri, True)
    for app in apps:
        for dm in app['domains']:
            if dm == domain:
                return app['id']

    return None

def get_app_config_by_id(client, app_id):
    return
    uri = f"applications?detail=1&partition_id={partition_id}"
    apps = client.get_all(uri, True)
    for app in apps:
        for dm in app['domains']:
            if dm['domain'] == domain:
                return app['id']

    return None

if __name__ == "__main__":
    rootCA_key, rootCA_crt, edge_node_key, edge_node_csr, edge_node_crt = generate_certificates(["test.com", "www.test.com"], "test.com")
    print(f"rootCA_key: {rootCA_key}\nrootCA_crt: {rootCA_crt}\nedge_node_key: {edge_node_key}\nedge_node_csr: {edge_node_csr}\n, edge_node_crt: {edge_node_crt}\n")
