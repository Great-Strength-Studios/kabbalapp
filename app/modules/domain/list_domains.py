from ...core import *
from ...domains import *
from . import *

def handle(context: MessageContext):

    # Retrieve app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get app domain service.
    domain_service: d.AppDomainService = context.services.domain_service(app_key)

    # Get domains.
    domains = domain_service.get_domains()

    # Return response.
    return domains   

