from ...core import *
from ...domains import *

def handle(context: MessageContext):

    # Unpack request.
    request: AddDomainModelProperty = context.data

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get app domain service.
    domain_service: d.AppDomainService = context.services.domain_service(app_key)

    # Format key if none is provided.
    if not request.key:
        request.key = request.name.lower().replace(' ', '_')

    # Set required to None if there is a default value.
    if request.default:
        request.required = None

    # Declare type property validation methods.

    # Validate type properties if they exist.
    type_properties = None
    if request.type_properties:
        from schematics.exceptions import DataError
        try:
            import json
            if request.type == 'str':
                type_properties = d.StringTypeProperties(json.loads(request.type_properties))
            elif request.type == 'date':
                type_properties = d.DateTypeProperties(json.loads(request.type_properties))
            elif request.type == 'datetime':
                type_properties = d.DateTimeTypeProperties(json.loads(request.type_properties))
        except DataError as e:
            raise AppError(context.errors.INVALID_TYPE_PROPERTIES.format_message(e.message))

    # Add property.
    property = domain_service.add_property(type_properties=type_properties, **request.to_primitive('domain.add_model_property'))

    # Raise app error if property is an error tuple.
    if isinstance(property, tuple):
        raise AppError(context.errors.get(property[0]).format_message(property[1]))

    # Return response.
    return property