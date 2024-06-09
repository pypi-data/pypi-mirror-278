import os
import fitz
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from .base import Plugin


def write_ico(input_img, output_img, size, dpi):
    drawing = svg2rlg(input_img)
    pdf = renderPDF.drawToString(drawing)
    doc = fitz.Document(stream=pdf)
    pix = doc.load_page(0).get_pixmap(alpha=True, dpi=dpi)
    dir_target = os.path.dirname(output_img)
    if not os.path.isdir(dir_target):
        os.makedirs(dir_target)
    pix.pil_save(output_img, sizes=[(size, size)])


class PluginFaviconIco(Plugin):
    favicon_ico_size = 128
    favicon_ico_dpi = 300

    def run(self):
        if not os.path.isfile(self.favicon_svg_filepath):
            return
        write_ico(self.favicon_svg_filepath, self.favicon_ico_filepath, self.favicon_ico_size, self.favicon_ico_dpi)

    @property
    def favicon_svg_filepath(self):
        return os.path.join(self.project_dir, 'res', 'favicon.svg')

    @property
    def favicon_ico_filepath(self):
        return os.path.join(self.project_dir, 'public', 'favicon.ico')
