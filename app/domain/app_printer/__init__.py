import os

from schematics import types as t, Model


class AppBlock(Model):

    file_path = t.StringType(required=True)
    code_block = t.StringType(required=True)
    code_lines = t.ListType(t.StringType, required=True)

    def update_code_block(self, code_block: str) -> None:
        self.code_block = code_block
        self.code_lines = code_block.splitlines()

    def update_code_line(self, line_index: int, code: str) -> None:
        self.code_lines[line_index] = code
        self.code_block = '\n'.join(self.code_lines)

class AppPrinter(object):

    def __init__(self, app_path: str):
        self.app_path = app_path
        
    def read_block(self, file_path: str) -> AppBlock:
        read_path = os.path.join(self.app_path, file_path)
        with open(read_path) as stream:
            code_block = stream.read()
            code_lines = code_block.splitlines()
        return AppBlock({
            'file_path': file_path,
            'code_block': code_block,
            'code_lines': code_lines
        })
        
    def print_block(self, app_path: str, code_block: AppBlock) -> None:
        write_path = os.path.join(self.app_path, code_block.file_path)
        with open(write_path, 'w') as stream:
            stream.write(code_block.code_block)