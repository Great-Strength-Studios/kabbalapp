from ...core import *
from ...domain import *

def handle(context: MessageContext):
    
    # Unpack request.
    name = context.data.name
    class_name = context.data.class_name

    # Get app project key.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)

    # Get domain repository.
    domain_repo: DomainRepository = context.services.domain_repo(app_key)

    # Get all value objects.
    value_objects = domain_repo.get_value_objects()

    # Create new value object instance.
    value_object = AppValueObject.create(name=name, class_name=class_name)

    # Check to see if value object already exists.
    exists = next((vo for vo in value_objects if vo.id == value_object.id), None)
    
    # Raise Value Object already exists error if value object already exists.
    if exists:
        raise AppError(context.errors.VALUE_OBJECT_ALREADY_EXISTS.format_message(value_object.class_name))

    # Add value object to domain and to value objects list.
    domain_repo.save_value_object(value_object)
    value_objects.append(value_object)

    # Get app project manager.
    app_project_manager: p.AppProjectManager = context.services.app_project_manager()

    # Get app project.
    app_project = app_project_manager.load_project(app_key)

    # Create value object block.
    value_object_block = ValueObjectBlock.create(app_project.app_directory, value_objects)

    # Add value object block to app project.
    with open(value_object_block.file_path, 'w') as f:
        f.write(value_object_block.print())

    # Return added value object.
    return value_object