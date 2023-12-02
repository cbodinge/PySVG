from fontTools.ttLib import TTFont
from base64 import b64encode
import inspect
import os
from pathlib import Path


class Font(dict):
    def __init__(self, family: str, weight: str):
        """
        This class is used by Text objects to define the fonts used by those objects.
        The fonts directory holds the TTF files and should be in the same directory as this module definition.

        :param family: string that defines the font family to use. Must match one of the folders in the fonts
        directory
        :param weight: Weight/Thickness of the font.
        The weight must match one of the files in the directory corresponding to family
        """

        file = weight + '.ttf'
        path = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        path = path / 'fonts' / family / file
        self.path = path
        font = TTFont(path)
        cmap = font['cmap'].getcmap(3, 1).cmap
        glyphs = font.getGlyphSet()
        self.units_per_em = font['head'].unitsPerEm
        self.family = family
        self.weight = weight

        super().__init__({_ord: glyphs[_chr].width for _ord, _chr in cmap.items()})
        self['.notdef'] = glyphs['.notdef']

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            return super().__getitem__('.notdef')

    def getBase64(self):
        with open(self.path, 'rb') as file:
            font = file.read()

        b64 = b64encode(font)
        return b64.decode('utf8')
