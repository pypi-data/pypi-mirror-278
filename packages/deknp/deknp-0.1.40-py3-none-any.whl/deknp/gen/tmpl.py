import functools
from pathlib import Path
from dektools.dict import sorted_dict
from dekgen.code.python.generator import CodeGenerator
from dektools.variables import get_user_email_from_git


class GeneratorBasic(CodeGenerator):
    TEMPLATE_DIR = Path(__file__).resolve().parent / 'templatefiles'

    def variables_data(self):
        return self.instance or {}


class ShellGenerator(GeneratorBasic):
    template_name = 'shell'
