from ...commands import *

def new_app_project(context, request, app_context, **kwargs):
    return NewAppProject({
        'id': request.get('id', None),
        'name': request.get('name', None),
        'app_directory': request.get('app_directory', None)
    })


def set_default_app_project(context, request, app_context, **kwargs):
    return SetDefaultAppProject({
        'id': request.get('id', None)
    })


def add_interface(context, request, app_context, **kwargs):
    return AddInterface({
        'name': request.get('name', None),
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
        'description': request.get('description', None),
        'base_type_model_id': request.get('base_type_model_id', None),
    })


def add_domain_model_attribute(context, request, app_context, **kwargs):
    type_properties_list = request.get('type_properties', [])
    if type_properties_list is None:
        type_properties_list = []
    type_properties = {}
    for type_property in type_properties_list:
        key, value = type_property.split('=')
        type_properties[key] = value

    return AddDomainModelAttribute({
        'parent_model_id': request.get('parent_model_id', None),
        'name': request.get('name', None),
        'type': request.get('type', 'str'),
        'inner_type': request.get('inner_type', None),
        'inner_type_model_id': request.get('inner_type_model_id', None),
        'poly_type_model_ids': request.get('poly_type_model_ids', None),
        'required': request.get('required', None),
        'default': request.get('default', None),
        'choices': request.get('choices', None),
        'description': request.get('description', None),
        'type_properties': type_properties
    })


def update_domain_model_attribute(context, request, app_context, **kwargs):
    # Map the values of the request dict to a new UpdateDomainModelAttribute object.
    # Set the values to None by default.
    return UpdateDomainModelAttribute({
        'model_id': request.get('model_id', None),
        'property_name': request.get('property_name', None),
        'property_setting': request.get('property_setting', None),
        'value': request.get('value', None)
    })


def remove_domain_model_property(context, request, app_context, **kwargs):
    return RemoveDomainModelProperty({
        'model_id': request.get('model_id', None),
        'property_name': request.get('property_name', None)
    })


def add_domain_method(context, request, app_context, **kwargs):
    # Map the values of the request dict to a new Add Domain Method request instance.
    return AddDomainMethod({
        'name': request.get('name', None),
        'type': request.get('type', None),
        'parent_id': request.get('parent_id', None),
        'description': request.get('description', None),
        'return_type': request.get('return_type', None),
        'inner_return_type': request.get('inner_return_type', None)
    })


def add_domain_method_parameter(context, request, app_context, **kwargs):
    # Map the values of the request dict to a new Add Domain Method Parameter request instance.
    return AddDomainMethodParameter({
        'parent_model_id': request.get('parent_model_id', None),
        'method_name': request.get('method_name', None),
        'name': request.get('name', None),
        'type': request.get('type', None),
        'inner_type': request.get('inner_type', None),
        'inner_type_model_id': request.get('inner_type_model_id', None),
        'required': request.get('required', None),
        'default': request.get('default', None),
        'description': request.get('description', None)
    })

def add_repository(context, request, app_context, **kwargs):
    # Map the values of the request dictionary to the AddRepository request.
    return AddRepository({
        'name': request.get('name', None),
        'class_name': request.get('class_name', None),
        'description': request.get('description', None)
    })

def add_repository_implementation(context, request, app_context, **kwargs):
    # Map the values of the request dictionary to the AddRepositoryImplementation request.
    return AddRepositoryImplementation({
        'name': request.get('name', None),
        'class_name': request.get('class_name', None),
        'repository_id': request.get('repository_id', None),
        'description': request.get('description', None)
    })

def print_domain_model_module(context, request, app_context, **kwargs):
    return PrintDomainModelModule()
