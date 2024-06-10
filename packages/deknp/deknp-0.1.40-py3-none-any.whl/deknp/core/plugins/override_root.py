import os
import tempfile
from dektools.file.operation import write_file, remove_path
from dekgen.tmpl.template import Template
from .base import Plugin


class PluginOverrideRootTemplate(Template):
    file_ignore_name = 'dek-override'


class PluginOverrideRoot(Plugin):
    template_cls = PluginOverrideRootTemplate

    override_key = 'override'
    dek_overrides_dir_name = 'dek-override'

    def run(self):
        ignore_info = self.merge_from_key(self.override_key)
        dir_temp = tempfile.mkdtemp()
        for dir_dek in self.dek_dir_list:
            src = os.path.join(dir_dek, self.dek_overrides_dir_name)
            if os.path.exists(src):
                write_file(dir_temp, ma=src)
        for filename, info in ignore_info.items():
            write_file(
                os.path.join(dir_temp, self.template_cls.get_file_ignore(filename)),
                s="\n".join([x for x, b in info.items() if b])
            )
        self.template_full.render_dir(self.project_dir, dir_temp, force_close_tpl=True)
        remove_path(dir_temp)
