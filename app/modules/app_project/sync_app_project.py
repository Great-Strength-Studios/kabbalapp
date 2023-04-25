from ...core import *

def handle(context: MessageContext):
    from ...domains import AppProjectManager, AppPrinter
    
    # Load request.
    request: SyncAppProject = context.data

    # Load local app printer.
    app_printer: AppPrinter = context.services.app_printer()

    # Load target app printer.
    target_app_printer: AppPrinter = context.services.app_printer(request.key)

    # Load app.
    target_app_printer.load_app()
