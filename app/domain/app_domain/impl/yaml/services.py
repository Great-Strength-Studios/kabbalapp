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
    
    def get_models(self, domain_key: str = None) -> List[AppDomainModel]:
        # Get domain if key is provided.
        if domain_key is not None:
            domain = self.get_domain(domain_key)
            # Return error if domain not found.
            if isinstance(domain, tuple):
                return domain
            # Return models.
            models = []
            for key, model_data in domain.models.items():
                model = AppDomainModel(raw_data=model_data)
                model.key = key
                models.append(model)
            return models
        # Get all models.
        domains = self.get_domains()
        models = []
        for domain in domains:
            for key, model_data in domain.models.items():
                model = AppDomainModel(raw_data=model_data)
                model.key = key
                models.append(model)
        return models

    
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