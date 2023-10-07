from ...commands import *

def new_app_project(context, request, app_context, **kwargs):
    return NewAppProject({
        'name': request.get('name', None),
        'key': request.get('key', None),
        'app_directory': request.get('app_directory', None)
    })

def set_default_app_project(context, request, app_context, **kwargs):
    return SetDefaultAppProject({
        'key': request.get('key', None)
    })

def add_interface(context, request, app_context, **kwargs):
    return AddInterface({
        'type': request.get('type', None)
    })

def add_cli_command(context, request, app_context, **kwargs):
    return AddCliCommand({
        'command_key': request.get('command_key', None),
        'subcommand_key': request.get('subcommand_key', None),
        'name': request.get('name', None),
        'description': request.get('description', None),
    })

def add_cli_parent_argument(context, request, app_context, **kwargs):
    return AddCliParentArgument({
        'name': request.get('name', None),
        'flags': request.get('flags', None),
        'positional': request.get('positional', False),
        'type': request.get('type', None),
        'default': request.get('default', None),
        'choices': request.get('choices', None),
        'nargs': request.get('nargs', None),
        'action': request.get('action', None),
        'description': request.get('description', None),
    })

def add_cli_argument(context, request, app_context, **kwargs):
    return AddCliArgument({
        'command_key': request.get('command_key', None),
        'subcommand_key': request.get('subcommand_key', None),
        'name': request.get('name', None),
        'flags': request.get('flags', None),
        'positional': request.get('positional', False),
        'type': request.get('type', None),
        'required': request.get('required', None),
        'default': request.get('default', None),
        'choices': request.get('choices', None),
        'nargs': request.get('nargs', None),
        'action': request.get('action', None),
        'description': request.get('description', None),
    })

def add_domain_model(context, request, app_context, **kwargs):
    return AddDomainModel({
        'name': request.get('name', None),
        'type': request.get('type', None),
        'class_name': request.get('class_name', None),
        'base_type_model_id': request.get('base_type_model_id', None),
    })

def add_domain_model_property(context, request, app_context, **kwargs):
    type_properties_list = request.get('type_properties', [])
    if type_properties_list is None:
        type_properties_list = []
    type_properties = {}
    for type_property in type_properties_list:
        key, value = type_property.split('=')
        type_properties[key] = value

    return AddDomainModelProperty({
        'model_id': request.get('model_id', None),
        'name': request.get('name', None),
        'type': request.get('type', 'str'),
        'inner_type': request.get('inner_type', None),
        'inner_type_model_id': request.get('inner_type_model_id', None),
        'required': request.get('required', None),
        'default': request.get('default', None),
        'choices': request.get('choices', None),
        'description': request.get('description', None),
        'type_properties': type_properties
    })

def print_domain_model_module(context, request, app_context, **kwargs):
    return PrintDomainModelModule()
