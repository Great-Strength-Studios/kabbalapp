from ...core import *
from ...domains import *

def handle(context: MessageContext):
	
	# Unpack request.
	request: ListDomainModels = context.data

	# Get app key from headers.
	app_key = context.headers.get('app_key', None)

	# If app key is not provided, raise exception.
	if not app_key:
		raise AppError(context.errors.APP_KEY_REQUIRED)
	
	# Get app domain service.
	domain_service: d.AppDomainService = context.services.domain_service(app_key)

	# Get domain models.
	domain_models = domain_service.list_models(**request.to_primitive())

	# Return models.
	return [model.to_primitive('list_domain_models') for model in domain_models]