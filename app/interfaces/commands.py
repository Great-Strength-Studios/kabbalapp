from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist

class RequestEvent(Model):
    pass


class NewAppProject(RequestEvent):
    
    id = t.StringType(required=True)
    name = t.StringType(required=True)
    app_directory = t.StringType(required=True)


class SetDefaultAppProject(RequestEvent):
    
    id = t.StringType(required=True)


class AddInterface(RequestEvent):
    
    name = t.StringType(required=True)
    type = t.StringType(required=True, choices=['cli', 'rest_flask'])


class AddCliCommand(RequestEvent):
    
    command_key = t.StringType(required=True)
    subcommand_key = t.StringType()
    name = t.StringType(required=True)
    help = t.StringType(required=True, deserialize_from=['help', 'description'])


class AddCliParentArgument(RequestEvent):
    
    name = t.StringType(required=True)
    help = t.StringType(required=True, deserialize_from=['help', 'description'])
    type = t.StringType(choices=['str', 'int', 'float'])
    flags = t.ListType(t.StringType(), default=[])
    positional = t.BooleanType(default=False)
    default = t.StringType()
    required = t.BooleanType()
    choices = t.ListType(t.StringType(), default=[])
    nargs = t.StringType()
    action = t.StringType()

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_parent_argument': blacklist('name', 'flags', 'positional'),
        }


class AddCliArgument(RequestEvent):
    
    command_key = t.StringType(required=True)
    subcommand_key = t.StringType()
    name = t.StringType(required=True)
    help = t.StringType(required=True, deserialize_from=['help', 'description'])
    type = t.StringType(choices=['str', 'int', 'float'])
    flags = t.ListType(t.StringType(), default=[])
    positional = t.BooleanType(default=False)
    default = t.StringType()
    required = t.BooleanType()
    choices = t.ListType(t.StringType(), default=[])
    nargs = t.StringType()
    action = t.StringType()

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_argument': blacklist('name', 'flags', 'positional'),
        }


class AddDomainModel(RequestEvent):
    
    name = t.StringType(required=True)
    type = t.StringType(required=True)
    class_name = t.StringType(required=True)
    description = t.StringType(required=True)
    base_type_model_id = t.StringType()


class AddDomainModelAttribute(RequestEvent):
    
    parent_model_id = t.StringType(required=True)
    name = t.StringType(required=True)
    type = t.StringType(default='str')
    inner_type = t.StringType()
    inner_type_model_id = t.StringType()
    poly_type_model_ids = t.ListType(t.StringType())
    required = t.BooleanType()
    default = t.StringType()
    choices = t.ListType(t.StringType())
    description = t.StringType()
    type_properties = t.DictType(t.StringType(), default={})

    class Options():
        roles = {
            'domain_model_attribute.create': blacklist('type_properties'),
        }


class UpdateDomainModelAttribute(RequestEvent):
    
    parent_model_id = t.StringType(required=True)
    attribute_name = t.StringType(required=True)
    attribute_setting = t.StringType(required=True, choices=['name', 'required', 'default', 'choices', 'description'])
    value = t.StringType()
    

class RemoveDomainModelAttribute(RequestEvent):
   
    parent_model_id = t.StringType(required=True)
    attribute_name = t.StringType(required=True)
    

class AddDomainMethod(RequestEvent):

    name = t.StringType(required=True)
    type = t.StringType(required=True, choices=['factory', 'behavior'])
    parent_id = t.StringType(required=True)
    description = t.StringType(required=True)
    return_type = t.StringType(choices=['str', 'int', 'float', 'bool', 'date', 'datetime', 'list', 'dict', 'model'])
    inner_return_type = t.StringType()
    
    class Options():
        roles = {
            'domain_method.create': blacklist('parent_id'),
        }

class AddDomainMethodParameter(RequestEvent):
    
    parent_model_id = t.StringType(required=True)
    method_name = t.StringType(required=True)
    name = t.StringType(required=True)
    type = t.StringType(required=True, choices=['str', 'int', 'float', 'bool', 'date', 'datetime', 'model'])
    description = t.StringType(required=True)
    inner_type = t.StringType()
    inner_type_model_id = t.StringType()
    required = t.BooleanType()
    default = t.StringType()
    
    class Options():
        roles = {
            'domain_method_parameter.create': blacklist('parent_model_id', 'method_name'),
        }

class AddRepository(RequestEvent):

    name = t.StringType(required=True)
    class_name = t.StringType(required=True)
    description = t.StringType(required=True)
    

class AddRepositoryImplementation(RequestEvent):

    name = t.StringType(required=True)
    class_name = t.StringType(required=True)
    repository_id = t.StringType(required=True)
    description = t.StringType(required=True)

    class Options():
        roles = {
            'app_repository_implementation.create': blacklist('repository_id'),
        }


class PrintDomainModelModule(RequestEvent):
    pass
