from ..events import *

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

def sync_app_project(context, request, app_context, **kwargs):
    return SyncAppProject({
        'key': request.get('key', None)
    })

def add_interface(context, request, app_context, **kwargs):
    return AddInterface({
        'key': request.get('key', None)
    })

def add_cli_command(context, request, app_context, **kwargs):
    return AddCliCommand({
        'key': request.get('key', None)
    })

def add_cli_parent_argument(context, request, app_context, **kwargs):
    return AddCliParentArgument({
        'key': request.get('key', None),
        'name': request.get('name', None),
        'flags': request.get('flags', None),
        'positional': request.get('positional', False),
        'type': request.get('type', None),
        'default': request.get('default', None),
        'choices': request.get('choices', None),
        'nargs': request.get('nargs', None),
        'action': request.get('action', None),
        'argument_help': request.get('argument_help', None),
    })

def add_cli_subcommand(context, request, app_context, **kwargs):
    return AddCliSubcommand({
        'command_key': request.get('command_key', None),
        'key': request.get('key', None),
        'name': request.get('name', None),
        'subcommand_help': request.get('subcommand_help', None),
    })

def add_domain(context, request, app_context, **kwargs):
    return AddDomain({
        'name': request.get('name', None),
        'key': request.get('key', None),
        'aliases': request.get('aliases', None),
    })

def sync_domain(context, request, app_context, **kwargs):
    return SyncDomain({
        'domain_key': request.get('domain_key', None),
        'force': request.get('force', False)
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

def update_domain(context, request, app_context, **kwargs):
    return UpdateDomain({
        'key': request.get('key', None),
        'name': request.get('name', None),
        'aliases': request.get('aliases', None),
    })

def add_domain_model(context, request, app_context, **kwargs):
    return AddDomainModel({
        'domain_key': request.get('domain_key', None),
        'name': request.get('name', None),
        'key': request.get('key', None),
        'class_name': request.get('class_name', None)
    })

def add_domain_role(context, request, app_context, **kwargs):
    return AddDomainRole({
        'domain_key': request.get('domain_key', None),
        'key': request.get('key', None),
        'type': request.get('type', None),
        'fields': request.get('fields', None)
    })

def add_domain_model_property(context, request, app_context, **kwargs):
    import json
    event = AddDomainModelProperty({
        'domain_key': request.get('domain_key', None),
        'model_key': request.get('model_key', None),
        'name': request.get('name', None),
        'key': request.get('key', None),
        'type': request.get('type', None)
    })
    try:
        event.metadata = json.loads(request.get('metadata', None))
    except:
        pass
    return event
