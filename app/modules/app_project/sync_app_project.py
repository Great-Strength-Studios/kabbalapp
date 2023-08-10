from ...core import *
from ...domain import *

def handle(context: MessageContext):    
    # Load request.
    request: SyncAppProject = context.data

    # Load local app printer.
    app_printer: AppPrinter = context.services.app_printer()

    # Load target app printer.
    target_app_printer: AppPrinter = context.services.app_printer(request.key)

    # Arrange packages/modules to be read.
    modules = [
        'app/core/config/__init__.py',
        'app/core/config/json.py',
        'app/core/config/yaml.py',
        'app/core/error.py',
        'app/core/routing.py',
        'app/core/__init__.py',
        'app/__init__.py'
    ]

    # Load blocks.
    blocks = [app_printer.read_block(module) for module in modules]

    # Write blocks.
    for block in blocks:
        target_app_printer.print_block(block)

    # Update project app config.
    import os, yaml
    app_project_manager: p.AppProjectManager = context.services.app_project_manager()
    app_project = app_project_manager.load_project(request.key)

    app_config = os.path.join(app_project.app_directory, 'app/app.yml')
    with open(app_config) as stream:
        app_config_data = yaml.safe_load(stream)

    modules_old = app_config_data.get('endpoints', None)
    # Exit this part if there are no endpoints (old format)
    if not modules_old:
        return
    
    modules_new = {}
    for key, value in modules_old.items():
        module_name, feature = key.split('.')
        functions = []
        try:
            for function in value.get('modules'):
                subdomain = function.pop('subdomain')
                module = function.pop('module')
                function_path = '{}.{}'.format(subdomain, module)
                function['function_path'] = function_path
                functions.append(function) 
        except TypeError:
            subdomain = value.pop('subdomain')
            module = value.pop('module')
            function_path = '{}.{}'.format(subdomain, module)
            value['function_path'] = function_path
            functions = [value]
        try:
            feature_data = {'functions': functions}
            modules_new[module_name]['features'][feature] = feature_data
            continue
        except KeyError:
            pass
        try:
            module_data = {'features': {feature: {'functions': functions}}}
            modules_new[module_name] = module_data
        except KeyError:
            pass
    app_config_data['modules'] = modules_new
    app_config_data['endpoints'] = None
    with open(app_config, 'w') as stream:
        yaml.safe_dump(app_config_data, stream, default_flow_style=False)