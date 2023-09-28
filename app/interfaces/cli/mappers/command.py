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

def add_value_object(context, request, app_context, **kwargs):
    return AddValueObject({
        'name': request.get('name', None),
        'class_name': request.get('class_name', None),
    })

def add_domain_implementation(context, request, app_context, **kwargs):
    return AddDomainImplementation({
        'domain_key': request.get('domain_key', None),
        'key': request.get('key', None),
        'name': request.get('name', None),
    })

def sync_domain_implementation(context, request, app_context, **kwargs):
    return SyncDomainImplementation({
        'domain_key': request.get('domain_key', None),
        'implementation_key': request.get('implementation_key', None),
        'force': request.get('force', False)
    })

def add_domain_model(context, request, app_context, **kwargs):
    return AddDomainModel({
        'domain_key': request.get('domain_key', None),
        'name': request.get('name', None),
        'key': request.get('key', None),
        'class_name': request.get('class_name', None)
    })

def list_domain_models(context, request, app_context, **kwargs):
    return ListDomainModels({
        'domain_key': request.get('domain_key', None),
    })

def add_domain_role(context, request, app_context, **kwargs):
    return AddDomainRole({
        'domain_key': request.get('domain_key', None),
        'key': request.get('key', None),
        'type': request.get('type', None),
        'fields': request.get('fields', None)
    })

def add_model_property(context, request, app_context, **kwargs):
    return AddModelProperty({
        'model_id': request.get('model_key', None),
        'name': request.get('name', None),
        'type': request.get('type', 'str'),
        'required': request.get('required', None),
        'default': request.get('default', None),
        'choices': request.get('choices', None),
        'serialized_name': request.get('serialized_name', None),
        'deserialize_from': request.get('deserialize_from', None),
        'description': request.get('description', None),
    })
