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
    if isinstance(dom, tuple):
        raise context.errors.get(dom[0]).format_message(dom[1])

    # Load app printer.
    printer: AppPrinter = context.services.app_printer(app_key)

    # Load app block to printer.
    app_block = printer.load_app()

    # Add new domain block to app block.
    domain_block = app_block.add_domain_block(dom.key)

    # Print app block.
    printer.print(domain_block, request.force)
