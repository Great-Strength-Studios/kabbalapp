from ...core import *
from ...domains import *

def handle(context: MessageContext):

    # Unpack request.
    request: SyncDomain = context.data

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise error if app key is not provided.
    if app_key is None:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get domain service.
    domain_service: DomainService = context.services.domain_service(app_key)

    # Get domain.
    dom: DomainEntity = domain.get_domain(domain_service, request.key)

    # Load app printer.
    printer: AppPrinter = context.services.app_printer(app_key)

    # Load app block.
    block = printer.read_app()
