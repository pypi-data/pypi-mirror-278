import os
import sys
import hashlib
import glob
import string
import json
import json5
from collections import OrderedDict
from dektools.file import read_text
from dektools.dict import flat, assign, dict_merge
from dekgen.tmpl.template import Template


class PluginBase:
    package_standard_name = 'package.json'
    package_dek_name = 'package.dek.json'
    node_modules_dir_name = 'node_modules'
    dek_path_generated = 'dek'

    def __init__(self, project_dir):
        self.project_dir = os.path.normpath(project_dir)

    def get_pkg_version(self, name):
        info = self.load_package_standard()
        version = (info.get('dependencies') or {}).get(name) or (info.get('devDependencies') or {}).get(name) or ''
        version = "".join([x for x in version if x in string.digits or x == '.'])
        return [int(x) for x in version.split('.')] if version else []

    def load_package_standard(self, default=None):
        if os.path.exists(self.package_standard_filepath):
            return self.load_json(self.package_standard_filepath)
        else:
            return default or {}

    def get_dek_path_generated(self, *args):
        return os.path.normpath(os.path.join(self.project_dir, self.dek_path_generated, *args))

    @classmethod
    def get_package_json(cls, filepath):
        data = {}
        package_path = os.path.join(filepath, cls.package_standard_name)
        package_dek_path = os.path.join(filepath, cls.package_dek_name)
        if os.path.isfile(package_path):
            data = cls.load_json(package_path)
        elif os.path.isfile(package_dek_path):
            data = cls.load_json(package_dek_path)
        return data

    @property
    def package_standard_filepath(self):
        return os.path.join(self.project_dir, self.package_standard_name)

    @property
    def package_dek_filepath(self):
        return os.path.join(self.project_dir, self.package_dek_name)

    @property
    def node_modules_dir(self):
        return os.path.join(self.project_dir, self.node_modules_dir_name)

    @staticmethod
    def log(*args):
        for arg in args:
            sys.stdout.write(str(arg))
            sys.stdout.write(' ')
        sys.stdout.write('\n')
        sys.stdout.flush()

    @staticmethod
    def get_data_uid(data):
        s = json.dumps(data, sort_keys=True)
        h = hashlib.sha256()
        h.update(s.encode('utf-8'))
        return h.hexdigest()

    @staticmethod
    def load_text(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def save_text(filepath, s):
        if os.path.exists(filepath):
            os.remove(filepath)
        dir_path = os.path.dirname(filepath)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(s)

    @classmethod
    def load_json(cls, filepath, ser=json):
        return ser.loads(cls.load_text(filepath), object_pairs_hook=OrderedDict)

    @classmethod
    def save_json(cls, filepath, data):
        cls.save_text(filepath, json.dumps(data, indent=4))


class Plugin(PluginBase):
    template_cls = Template

    def __init__(self, project_dir, dek_info_list, dek_dir_list, dek_dev_dir_list, share_data):
        super().__init__(project_dir)
        self.dek_info_list = dek_info_list
        self.dek_dir_list = [os.path.normpath(p) for p in dek_dir_list]
        self.dek_dev_dir_list = [os.path.normpath(p) for p in dek_dev_dir_list]
        self.share_data = share_data

    def run(self):
        raise NotImplemented()

    @staticmethod
    def flat_variables(d):
        return flat(d, '__')

    def get_variables(self):
        data_package_standard = self.load_package_standard()
        variables = dict(
            package=dict(
                name=data_package_standard['name'],
                version=data_package_standard['version'],
                description=data_package_standard['description']
            )
        )
        for dek in self.dek_info_list:
            variables = assign(variables, dek.get('vars') or {})
        variables = assign(variables, self.share_data.get('variables') or {})
        return variables

    def merge_from_key(self, key):
        result = OrderedDict()
        for data in self.dek_info_list:
            env_set = data.get(key)
            if env_set:
                dict_merge(result, env_set)
        return result

    @property
    def dek_dir_list_for_scan(self):
        dir_list = [d for d in self.dek_dir_list if d != self.project_dir]
        for d in os.listdir(self.project_dir):
            fp = os.path.join(self.project_dir, d)
            if os.path.isdir(fp) and d not in ['dist', 'build', self.node_modules_dir_name, self.dek_path_generated]:
                dir_list.append(fp)
        return dir_list

    @property
    def template_full(self):
        return self.template_cls(self.flat_variables(self.get_variables()))

    def render_json(self, data):
        return json.loads(self.template_full.render(json.dumps(data)), object_pairs_hook=OrderedDict)

    def list_glob_filepath(self, glob_item):
        for dir_scan in self.dek_dir_list_for_scan:
            for filepath in glob.glob(dir_scan + glob_item, recursive=True):
                yield filepath

    def get_js_glob_list(self):
        import_meta_glob = 'import.meta.glob'
        glob_list = set()
        for filepath in self.list_glob_filepath('/**/*.js'):
            js = read_text(filepath)
            index = 0
            while index < len(js):
                index = js.find(import_meta_glob, index)
                if index != -1:
                    index += len(import_meta_glob)
                    begin = None
                    end = None
                    while index < len(js):
                        if js[index] in '"\'':
                            if begin is None:
                                begin = index
                            elif end is None:
                                end = index
                                break
                        index += 1
                    glob_list.add(js[begin + 1:end])
                else:
                    break
        return glob_list


class PluginVue(Plugin):
    def get_vue_version(self):
        return self.get_pkg_version('vue')


class PluginUniapp(Plugin):
    manifest_name = 'manifest.json'

    @property
    def manifest_filepath(self):
        return os.path.join(self.project_dir, self.manifest_name)

    def is_uniapp_project(self):
        return os.path.isfile(self.manifest_filepath)

    def get_uniapp_vue_version(self):
        data = self.load_json(self.manifest_filepath, json5)
        version = data.get('vueVersion')
        if version:
            return int(version)
        return None
