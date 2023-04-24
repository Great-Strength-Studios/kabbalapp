from ..events import *

def new_app_project(context, request, app_context, **kwargs):
    return NewAppProject({
        'name': request.get('name', None),
        'app_key': request.get('app_key', None),
        'app_directory': request.get('app_directory', None)
    })

def sync_app_project(context, request, app_context, **kwargs):
    return SyncAppProject({
        'app_key': request.get('app_key', None)
    })

def add_domain(context, request, app_context, **kwargs):
    return AddDomain({
        'name': request.get('name', None),
        'key': request.get('key', None),
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