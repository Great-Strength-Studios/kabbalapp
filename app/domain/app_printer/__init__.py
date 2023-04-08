from schematics import types as t, Model


class AppBlock(Model):

    file_path = t.StringType(required=True)
    code_block = t.StringType(required=True)


class AppPrinter(object):
    
    def read_block(self, file_path: str) -> AppBlock:
        pass
        
    def print_block(self, file_path: str, code_block: AppBlock) -> None:
        pass