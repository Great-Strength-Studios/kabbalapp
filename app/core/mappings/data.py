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
    name = request.get('domain_name', None)
    key = request.get('domain_key', None)
    if name and not key:
        key = name.lower().replace(' ', '_')
    return AddDomain({
        'name': name,
        'key': key,
    })