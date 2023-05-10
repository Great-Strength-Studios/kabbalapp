from ...services import *
from .models import *

class YamlAppDomainService(AppDomainService):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)

    def add_domain(self, key: str, name: str, aliases: List[str]) -> AppDomain:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        domain_data = { 'name': name, 'aliases': aliases }
        try:
            if data['domains'] is not None and key in data['domains']:
                return ('DOMAIN_ALREADY_EXISTS', key)
            if data['domains'] is None:
                data['domains'] = {key: domain_data}
            else:
                data['domains'][key] = domain_data
        except KeyError:
            data['domains'] = {key: domain_data}
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'key': key,
            'name': name
        }
        return AppDomain(raw_data=raw_data)
    
    def get_domain(self, key: str) -> AppDomain:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        if data['domains'] is not None and key in data['domains']:
            domain_data = data['domains'][key]
            raw_data = {
                'key': key,
                'name': domain_data.get('name'),
                'aliases': domain_data.get('aliases', []),
                'models': domain_data.get('models', {}),
                'impl': domain_data.get('impl', {})
            }
            return AppDomain(raw_data=raw_data)
        else:
            return ('DOMAIN_NOT_FOUND', key)
        
    def update_domain(self, key: str, name: str = None, aliases: List[str] = None) -> AppDomain:
        import yaml
        # Retrieve existing domain.
        domain = self.get_domain(key)
        # Return error if domain not found.
        if isinstance(domain, tuple):
            return domain
        # Update domain.
        if name is not None:
            domain.name = name
        if aliases is not None:
            domain.aliases = aliases
        # Save domain.
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        data['domains'][key] = domain.to_primitive('update')
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        return domain
    
    def add_implementation(self, domain_key: str, name: str, key: str) -> AppDomainImplementation:
        import yaml
        domain = self.get_domain(domain_key)
        if isinstance(domain, tuple):
            return domain
        impl = AppDomainImplementation(raw_data={'name': name, 'key': key})
        if key in domain.impl:
            return ('DOMAIN_IMPLEMENTATION_ALREADY_EXISTS', key) 
        domain.impl[key] = impl
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        data['domains'][domain_key] = domain.to_primitive('update')
        with open(self.schema_file_path, 'w') as f:
            yaml.safe_dump(data, f)
        return impl
    
    def get_implementation(self, domain_key: str, implementation_key: str) -> AppDomainImplementation:
        import yaml
        domain = self.get_domain(domain_key)
        if isinstance(domain, tuple):
            return domain
        if implementation_key in domain.impl:
            impl = AppDomainImplementation(domain.impl[implementation_key])
            impl.key = implementation_key
            return impl
        else:
            return ('DOMAIN_IMPLEMENTATION_NOT_FOUND', implementation_key)

    
    def add_model(self, domain_key: str, key: str, name: str, class_name: str) -> AppDomainModel:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        model_data = {'name': name, 'class_name': class_name}
        if data['domains'] is not None and domain_key in data['domains']:
            try:
                if data['domains'][domain_key]['models'] is not None and key in data['domains'][domain_key]['models']:
                    return ('DOMAIN_MODEL_ALREADY_EXISTS', key)
                if data['domains'][domain_key]['models'] is None:
                    data['domains'][domain_key]['models'] = {key: model_data}
                else:
                    data['domains'][domain_key]['models'][key] = model_data
            except KeyError:
                data['domains'][domain_key]['models'] = {key: model_data}
        else:
            return ('DOMAIN_NOT_FOUND', domain_key)
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'name': name,
            'class_name': class_name
        }
        return AppDomainModel(raw_data=raw_data)
    
    def get_model(self, domain_key: str, key: str) -> AppDomainModel:
        # Get domain.
        domain = self.get_domain(domain_key)
        # Return error if domain not found.
        if isinstance(domain, tuple):
            return domain
        # Return error if model not found.
        if key not in domain.models:
            return ('DOMAIN_MODEL_NOT_FOUND', key)
        # Return model.
        model = domain.models[key]
        model.key = key
        return model
    
    def add_role(self, domain_key: str, key: str, role_type: str, role_fields: List[str]) -> AppDomainRole:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        role_data = {'type': role_type, 'fields': role_fields}
        if data['domains'] is not None and domain_key in data['domains']:
            try:
                if data['domains'][domain_key]['roles'] is not None and key in data['domains'][domain_key]['roles']:
                    return ('DOMAIN_ROLE_ALREADY_EXISTS', key)
                if data['domains'][domain_key]['roles'] is None:
                    data['domains'][domain_key]['roles'] = {key: role_data}
                else:
                    data['domains'][domain_key]['roles'][key] = role_data
            except KeyError:
                data['domains'][domain_key]['roles'] = {key: role_data}
        else:
            return ('DOMAIN_NOT_FOUND', domain_key)
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'type': role_type,
            'fields': role_fields
        }
        return AppDomainRole(raw_data=raw_data)
    
    def add_property(self, domain_key: str, model_key: str, key: str, name: str, type: str, type_properties: TypeProperties = None, **kwargs) -> AppDomainModelProperty:
        import yaml
        # Get domain model.
        model = self.get_model(domain_key, model_key)
        # Return error if domain or model not found.
        if isinstance(model, tuple):
            return model
        # Return error if property already exists.
        if key in model.properties:
            return ('DOMAIN_MODEL_PROPERTY_ALREADY_EXISTS', key)
        # Format property data.
        property = YamlAppDomainModelProperty({'key': key, 'name': name, 'type': type, **kwargs})
        # Add property data to model if properties is None.
        if model.properties is None:
            model.properties = {}
        # Add property to model.
        model.properties[key] = property  
        # Read schema file.
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        # Update schema file.
        data['domains'][domain_key]['models'][model_key] = model.to_primitive('domain.add_property')
        # Write updates to schema file.
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        # Return property.
        return property