from pathlib import Path as P
from fontTools.ttLib import TTFont


class Font:
    def __init__(self, family: str, size: int, weight: str):
        """
        This class is used by Text objects to define the fonts used by those objects.
        The fonts directory holds the TTF files and should be in the same directory as this module definition.

        :param family: string that defines the font family to use. Must match one of the folders in the fonts
        directory
        :param size: Point size of the font
        :param weight: Weight/Thickness of the font. The weight must match one of the files in the directory corresponding to family
        """

        # Searches Working Directory for font path
        # path is parent/fonts/family/weight.ttf
        # Currently only formatted for truetype fonts
        path = P.cwd()
        file = weight + '.ttf'
        path = path / 'fonts' / family / file
        font = TTFont(path)
        self.cmap = font['cmap'].getcmap(3, 1).cmap
        self.glyph_set = font.getGlyphSet()
        self.units_per_em = font['head'].unitsPerEm
        self.size = size
        self.family = family
        self.weight = weight

    def copy(self):
        """
        Creates a new instance of this class with identical parameters.

        :return: a copy of this class as a new instance
        :rtype: Font
        """
        font = Font(self.family, self.size, self.weight)

        return font

    def getTextWidth(self, text: str):
        """
        Calculates the width of the string in pixels.

        :param text: the string to determine the width of.
        :return: the string width
        :rtype: float
        """
        total = 0
        for character in text:
            if ord(character) in self.cmap and self.cmap[ord(character)] in self.glyph_set:
                total += self.glyph_set[self.cmap[ord(character)]].width
            else:
                total += self.glyph_set['.notdef'].width
        total = total * float(self.size) / self.units_per_em

        return total
