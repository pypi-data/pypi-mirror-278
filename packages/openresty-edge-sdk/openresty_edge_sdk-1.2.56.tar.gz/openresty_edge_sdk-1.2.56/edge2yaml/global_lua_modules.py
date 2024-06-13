from .utils import error, warn, info, md5sum, fix_line
from .read_config import read_lua_modules


def cleanup_global_lua_modules(client, partition_id):
    modules = client.get_all_partition_lua_module(partition_id)
    for mod in modules:
        if 'id' in mod:
            info(f"removing global lua module, partition id: {partition_id}, module id: {mod['id']}")
            client.del_partition_lua_module(partition_id, mod['id'])

def process_global_lua_modules(client, partition_id, location, configs_path):
    # read local lua modules
    new_lua_modules = read_lua_modules(configs_path, location)
    if not new_lua_modules:
        error(f"no lua modules were found in directory \"{location}\". if you want to delete lua modules from Edge Admin, please use the cleanup option.")

    info("checking if lua modules have changed")

    # get old lua module
    old_lua_modules = client.get_all_partition_lua_module(partition_id)
    old_lua_module_names = {}
    # check if lua module changed
    if old_lua_modules:
        for mod in old_lua_modules:
            # print(mod)
            old_lua_module_names[mod['name']] = mod

    # update or insert lua module
    sorted_filenames = sorted(new_lua_modules.keys())
    for mod_name in sorted_filenames:
        mod_code = new_lua_modules[mod_name]
        if mod_name in old_lua_module_names:
            # check md5
            old_mod = old_lua_module_names[mod_name]
            if md5sum(mod_code) == md5sum(old_mod['code']):
                # check next module
                # info(f"global lua module have not changed, file: {mod_name}.lua")
                continue
            else:
                # update
                try:
                    info(f"updating global lua module, file: {mod_name}.lua")
                    client.put_partition_lua_module(partition_id, old_mod['id'], mod_name, mod_code)
                except Exception as e:
                    error(f"failed to update global lua module, file: {mod_name}.lua", e)
        else:
            # insert
            try:
                info(f"adding global lua module: {mod_name}.lua")
                client.new_partition_lua_module(partition_id, mod_name, mod_code)
            except Exception as e:
                error(f"failed to add lua module, file: {mod_name}.lua", e)
