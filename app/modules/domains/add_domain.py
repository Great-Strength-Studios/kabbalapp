from ...core import *
from ...domains import *

def handle(context: MessageContext):

    # Get request event.
    request: AddDomain = context.data

    # Get domain service.
    service: DomainService = context.services.domain_service()

    # Create domain key if none exists.
    if not request.key:
        request.key = request.name.to_lower().replace(' ', '-')
    
    # Add domain.
    domain = service.add_domain(request.name, request.key)

    # Return domain.
    return domain