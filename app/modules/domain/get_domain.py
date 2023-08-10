from ...core import *
from ...domain import *

def handle(context: MessageContext):
	
	# Unpack request.
	request: GetDomain = context.data

	# Get app key from headers.
	app_key = context.headers.get('app_key', None)

	# If app key is not provided, raise exception.
	if not app_key:
		raise AppError(context.errors.APP_KEY_REQUIRED)
	
	# Get app domain service.
	domain_service: d.AppDomainService = context.services.domain_service(app_key)

	# Get domain.
	domain = domain_service.get_domain(request.key)

	# If domain is an error tuple, raise exception.
	if isinstance(domain, tuple):
		raise AppError(context.errors.get(domain[0]).format_message(domain[1]))
	
	# Return domain.
	return domain