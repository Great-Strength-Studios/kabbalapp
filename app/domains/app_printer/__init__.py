import os, shutil

from schematics import types as t, Model

class AppImport(Model):

    class ImportName(Model):
        name = t.StringType(required=True)
        alias = t.StringType(default=None)

    names = t.ListType(t.ModelType(ImportName), required=True)
    path = t.StringType()

    def format(self):
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

    def format(self):
        return f'{self.name.lower()} = {self.value}'
    
class AppConstant(AppVariable):
    def format(self):
        return f'{self.name.upper()} = {self.value}'
    
class KabbalappVersion(AppVariable):
    def __init__(self, value: str):
        super().__init__({
            'name': '__kabbalapp_version__',
            'value': value
        })


class AppModule(Model):

    name = t.StringType(required=True)
    key = t.StringType(required=True)
    file_path = t.StringType(required=True)
    code_block = t.StringType(default='')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        code_lines = self.code_block.splitlines()

    def update_code_block(self, code_block: str) -> None:
        self.code_block = code_block
        self.code_lines = code_block.splitlines()

    def update_code_line(self, line_index: int, code: str) -> None:
        self.code_lines[line_index] = code
        self.code_block = '\n'.join(self.code_lines)

    def print(self, app_path: str):
        write_path = os.path.join(app_path, self.file_path)
        with open(write_path, 'w') as stream:
            stream.write(self.code_block)

class AppPackageBlock(Model):
    package_name = t.StringType(required=True)
    parent_path = t.StringType(required=True)

    def print(self, force: bool = False):
        package_path = os.path.join(self.parent_path, self.package_name)
        os.makedirs(package_path, exists_ok=True)
        if os.path.exists(os.path.join(package_path, '__init__.py')) and not force:
            return
        with open(os.path.join(package_path, '__init__.py'), 'w') as stream:
            stream.write('')

class AppDomainBlock(AppPackageBlock):

    def __init__(self, domain_key: str, **kwargs):
        raw_data = kwargs.get('raw_data', {})
        raw_data['package_name'] = domain_key
        super().__init__(**kwargs)


    def print(self, app_path: str, force: bool = False):
        package_path = os.path.join(app_path, self.parent_path, self.package_name)
        os.makedirs(package_path, exist_ok=True)
        domain_modules = ['__init__.py', 'core.py', 'entities.py']
        for module in domain_modules:
            module_path = os.path.join(package_path, module)
            if not os.path.exists(module_path) or force:
                with open(module_path, 'w') as stream:
                    stream.write('')

    def read(self, app_path: str):
        pass

class AppBlock(AppPackageBlock):

    domain_blocks = t.DictType(t.StringType(), t.ModelType(AppDomainBlock), default={})

    def add_domain_block(self, domain_key: str) -> AppDomainBlock:
        domain_block = AppDomainBlock(domain_key, raw_data={
            'parent_path': os.path.join(self.parent_path, self.package_name, 'domains')
        })
        self.domain_blocks[domain_key] = domain_block
        return domain_block
    
    def get_domain_block(self, domain_key: str) -> AppDomainBlock:
        return self.domain_blocks.get(domain_key)

    def read(self, app_path: str):
        package_files = os.listdir(os.path.join(self.parent_path, self.package_name))
        for package_file in package_files:
            if package_file == 'domains':
                domains_path = os.path.join(self.parent_path, self.package_name, package_file)
                domain_files = os.listdir(domains_path)
                for domain_file in domain_files:
                    if os.path.splitext(domain_file)[1] == '.py' or domain_file == '__pycache__':
                        continue
                    domain_block = self.add_domain_block(domain_file)
                    domain_block.read(app_path)
                    self.domain_blocks[domain_file] = domain_block
    
    def print(self, app_path: str, force: bool = False):
        package_path = os.path.join(app_path, self.parent_path, self.package_name)
        os.makedirs(package_path, exists_ok=True)
        if os.path.exists(os.path.join(package_path, '__init__.py')) and not force:
            return
        with open(os.path.join(package_path, '__init__.py'), 'w') as stream:
            stream.write('')

class AppPrinter(object):


    def __init__(self, app_path: str):
        self.app_path = app_path

    def load_app(self) -> AppBlock:
        app_block = AppBlock({
            'package_name': 'app',
            'parent_path': self.app_path
        })
        app_block.read(self.app_path)
        return app_block

    def add_package_block(self, package_name: str, parent_path: str = None) -> AppPackageBlock:
        package_block = AppPackageBlock({
            'package_name': package_name,
            'parent_path': parent_path,
        })
        return package_block
        
    def read_block(self, file_path: str) -> AppModuleBlock:
        read_path = os.path.join(self.app_path, file_path)
        with open(read_path) as stream:
            code_block = stream.read()
            code_lines = code_block.splitlines()
        return AppModuleBlock({
            'file_path': file_path,
            'code_block': code_block,
            'code_lines': code_lines
        })
    
    def print(self, block, force: bool = False) -> None:
        block.print(self.app_path, force)
        
    def print_block(self, code_block: AppModuleBlock, app_path: str = None) -> None:
        if not app_path:
            app_path = self.app_path
        write_path = os.path.join(app_path, code_block.file_path)
        os.makedirs(os.path.dirname(write_path), exist_ok=True)
        with open(write_path, 'w') as stream:
            stream.write(code_block.code_block)