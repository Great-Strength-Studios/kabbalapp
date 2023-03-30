import os
import yaml

from app.constants import *


root_dir = os.getcwd()
app_dir = os.path.join(root_dir, APP_DIR_NAME)


def write_file(path, content):
    with open(path, 'w') as w:
        if not content:
            return
        if content[0] == '\n':
            content = content[1:]
        if content[-1] == '\n':
            content = content[:-1]
        w.write(content)

# Print requirements file
requirements = os.path.join(root_dir, REQUIREMENTS_FILE)
if not os.path.exists(requirements):
    write_file(requirements, REQUIREMENTS_CONTENT)

# Make app directory if it does not exist.
if not os.path.exists(app_dir):
    os.mkdir(app_dir)

    # Write init file
    app_dir_init = os.path.join(app_dir, INIT_FILE)
    write_file(app_dir_init, APP_INIT_CONTENT)

    app_dir_config = os.path.join(app_dir, APP_CONFIG_FILE)
    with open(app_dir_config, 'w') as write:
        yaml.safe_dump(APP_CONFIG_CONTENT, write)

    app_dir_constants = os.path.join(app_dir, APP_CONSTANTS_FILE)
    write_file(app_dir_constants, APP_CONSTANTS_CONTENT)

core_dir = os.path.join(app_dir, CORE_DIR_NAME)
if not os.path.exists(core_dir):
    os.mkdir(core_dir)

    write_file(os.path.join(core_dir, INIT_FILE), CORE_INIT_CONTENT)

core_mappings_dir = os.path.join(core_dir, CORE_MAPPINGS_DIR_NAME)
if not os.path.exists(core_mappings_dir):
    os.mkdir(core_mappings_dir)

    core_mappings_data = os.path.join(core_mappings_dir, CORE_MAPPINGS_DATA_FILE)
    write_file(core_mappings_data, CORE_MAPPINGS_DATA_CONTENT)

    core_mappings_headers = os.path.join(core_mappings_dir, CORE_MAPPINGS_HEADERS_FILE)
    write_file(core_mappings_headers, CORE_MAPPINGS_HEADERS_CONTENT)

    core_mappings_services = os.path.join(core_mappings_dir, CORE_MAPPINGS_SERVICES_FILE)
    write_file(core_mappings_services, None)

core_activity = os.path.join(core_dir, CORE_ACTIVITY_FILE)
if not os.path.exists(core_activity):
    write_file(core_activity, CORE_ACTIVITY_CONTENT)

core_containers = os.path.join(core_dir, CORE_CONTAINERS_FILE)
if not os.path.exists(core_containers):
    write_file(core_containers, CORE_CONTAINERS_CONTENT)

core_error = os.path.join(core_dir, CORE_ERROR_FILE)
if not os.path.exists(core_error):
    write_file(core_error, CORE_ERROR_CONTENT)

core_events = os.path.join(core_dir, CORE_EVENTS_FILE)
if not os.path.exists(core_events):
    write_file(core_events, CORE_EVENTS_CONTENT)

core_routing = os.path.join(core_dir, CORE_ROUTING_FILE)
if not os.path.exists(core_routing):
    write_file(core_routing, CORE_ROUTING_CONTENT)

endpoints_dir = os.path.join(app_dir, ENDPOINTS_DIR_NAME)
if not os.path.exists(endpoints_dir):
    os.mkdir(endpoints_dir)

    write_file(os.path.join(endpoints_dir, INIT_FILE), None)

modules_dir = os.path.join(app_dir, MODULES_DIR_NAME)
if not os.path.exists(modules_dir):
    os.mkdir(modules_dir)

    write_file(os.path.join(modules_dir, INIT_FILE), None)

services_dir = os.path.join(app_dir, SERVICES_DIR_NAME)
if not os.path.exists(services_dir):
    os.mkdir(services_dir)

    write_file(os.path.join(services_dir, INIT_FILE), None)