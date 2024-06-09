from dektools.dict import assign
from .base import Plugin


class PluginPackageJson(Plugin):
    def run(self):
        for data in self.dek_info_list:
            package_json = data.get(self.package_standard_name) or {}
            if package_json:
                package_json = self.render_json(package_json)
                d = self.load_package_standard()
                d = assign(d, package_json)
                d.pop('dek', None)
                self.save_json(self.package_standard_filepath, d)
