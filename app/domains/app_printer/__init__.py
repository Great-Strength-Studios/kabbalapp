import os, shutil
from typing import List
from schematics import types as t, Model
from schematics.types.serializable import serializable



class AppImport(Model):

    def __init__(self, line: str, **kwargs):
        if line.startswith('from'):
            path, raw_names = line.split('from')[1].split('import')
        else:
            raw_names = line.split('import')[1]
            path = None
        names = []
        for name in raw_names.split(','):
            name = name.strip()
            if 'as' in name:
                name, alias = name.split('as')
                names.append({
                    'name': name.strip(),
                    'alias': alias.strip()
                })
            else:
                names.append({
                    'name': name,
                    'alias': None
                })
        raw_data = {
            'names': names,
            'path': path
        }
        super().__init__(raw_data=raw_data, **kwargs)

    class ImportName(Model):
        name = t.StringType(required=True)
        alias = t.StringType(default=None)

    names = t.ListType(t.ModelType(ImportName), required=True)
    path = t.StringType()

    @serializable
    def formatted(self):
        formatted_names = []
        for name in self.names:
            if name.alias:
                formatted_names.append(f'{name.name} as {name.alias}')
            else:
                formatted_names.append(name.name)
        if self.path:
            return f'from {self.path} import {", ".join(formatted_names)}'
        else:
            return f'import {", ".join(formatted_names)}'
        
class AppVariable(Model):
    name = t.StringType(required=True)
    value = t.StringType(required=True)

    @serializable
    def formatted(self):
        return f'{self.name.lower()} = {self.value}'

class AppConstant(AppVariable):
    @serializable
    def formatted(self):
        return f'{self.name.upper()} = {self.value}'
    
class KabbalappVersion(AppVariable):
    def __init__(self, value: str):
        super().__init__({
            'name': '__kabbalapp_version__',
            'value': value
        })

class AppModule(Model):

    name = t.StringType(required=True)
    parent_path = t.StringType(required=True)
    standard_imports = t.ListType(t.ModelType(AppImport), default=[])

    def __init__(self, name: str, parent_path: str, **kwargs):
        raw_data = {
            'name': name,
            'parent_path': parent_path
        }
        super().__init__(raw_data=raw_data, **kwargs)


    @serializable
    def full_path(self) -> str:
        return os.path.join(self.parent_path, self.name)
    
    @serializable
    def content(self) -> str:
        with open(self.full_path, 'r') as stream:
            return stream.read()
        
    @property
    def lines(self) -> List[str]:
        return self.content.splitlines()

    def print(self):
        with open(self.full_path, 'w') as stream:
            stream.write(self.content)


class AppPackage(Model):
    name = t.StringType(required=True)
    parent_path = t.StringType(required=True)

    def __init__(self, name: str, parent_path: str, **kwargs):
        raw_data = {
            'name': name,
            'parent_path': parent_path
        }
        super().__init__(raw_data=raw_data, **kwargs)

    def print(self, force: bool = False):
        package_path = os.path.join(self.parent_path, self.name)
        os.makedirs(package_path, exists_ok=True)
        if os.path.exists(os.path.join(package_path, '__init__.py')) and not force:
            return
        with open(os.path.join(package_path, '__init__.py'), 'w') as stream:
            stream.write('')

class DomainsPackage(AppPackage):
    pass

class AppDomainPackage(AppPackage):
    pass

class MainAppPackage(AppPackage):

    class AppInitModule(AppModule):
        kabbalapp_version = t.ModelType(KabbalappVersion, required=True)
        imports = t.ListType(t.ModelType(AppImport), default=[])

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            for line in self.lines:
                if line.startswith('from') or line.startswith('import'):
                    self.imports.append(AppImport(line))
                elif line.startswith('__kabbalapp_version__'):
                    self.kabbalapp_version = KabbalappVersion(line.split('=')[1].strip())

    init_module = t.ModelType(AppInitModule, required=True)
    constants_module = t.ModelType(AppModule, required=True)
    domains_package = t.ModelType(DomainsPackage, required=True)

    def __init__(self, name: str, parent_path: str, **kwargs):
        raw_data = {
            'name': name,
            'parent_path': parent_path
        }
        super().__init__(name=name, parent_path=parent_path, **kwargs)
        self.init_module = self.AppInitModule(
            name='__init__.py',
            parent_path=os.path.join(self.parent_path, self.name)
        )
        self.constants_module = AppModule(
            name='constants.py',
            parent_path=os.path.join(self.parent_path, self.name)
        )
        self.domains_package = DomainsPackage(
            name='domains',
            parent_path=os.path.join(self.parent_path, self.name)
        )

    def add_domain_block(self, domain_key: str) -> AppDomainPackage:
        domain_block = AppDomainPackage(domain_key, raw_data={
            'parent_path': os.path.join(self.parent_path, self.name, 'domains')
        })
        self.domain_blocks[domain_key] = domain_block
        return domain_block
    
    def get_domain_block(self, domain_key: str) -> AppDomainPackage:
        return self.domain_blocks.get(domain_key)
    
    def print(self, app_path: str, force: bool = False):
        package_path = os.path.join(app_path, self.parent_path, self.name)
        os.makedirs(package_path, exists_ok=True)
        if os.path.exists(os.path.join(package_path, '__init__.py')) and not force:
            return
        with open(os.path.join(package_path, '__init__.py'), 'w') as stream:
            stream.write('')

class AppPrinter(object):


    def __init__(self, app_path: str):
        self.app_path = app_path

    def load_app(self) -> MainAppPackage:
        app_block = MainAppPackage(
            name='app',
            parent_path=self.app_path
        )
        return app_block

    def add_package_block(self, name: str, parent_path: str = None) -> AppPackage:
        package_block = AppPackage({
            'name': name,
            'parent_path': parent_path,
        })
        return package_block
        
    def read_block(self, file_path: str) -> AppModule:
        read_path = os.path.join(self.app_path, file_path)
        with open(read_path) as stream:
            code_block = stream.read()
            code_lines = code_block.splitlines()
        return AppModule({
            'file_path': file_path,
            'code_block': code_block,
            'code_lines': code_lines
        })
    
    def print(self, block, force: bool = False) -> None:
        block.print(self.app_path, force)
        
    def print_block(self, code_block: AppModule, app_path: str = None) -> None:
        if not app_path:
            app_path = self.app_path
        write_path = os.path.join(app_path, code_block.file_path)
        os.makedirs(os.path.dirname(write_path), exist_ok=True)
        with open(write_path, 'w') as stream:
            stream.write(code_block.code_block)