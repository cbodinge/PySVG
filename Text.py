from Paths import Path
from pathlib import Path as P
from fontTools.ttLib import TTFont


class Text(Path):
    def __init__(self):
        super().__init__()
        self.text = ''
        self.x = 0
        self.y = 0
        self.angle = 0
        self.font = None

        self._baseline = None
        self._anchor = None

    @property
    def baseline(self):
        return self._baseline

    @baseline.setter
    def baseline(self, baseline: str):
        options = ['auto', 'text-bottom', 'alphabetic', 'ideographic', 'middle', 'central', 'mathematical', 'hanging',
                   'text-top']

        if baseline in options:
            self._baseline = baseline

    @property
    def anchor(self):
        """
        controls how the text is drawn relative to the x coordinate. Similar to left, center, right alignment.
        """
        return self._anchor

    @anchor.setter
    def anchor(self, anchor: str):
        options = ['start', 'middle', 'end']

        if anchor in options:
            self._anchor = anchor

    def copy(self, item=None):
        if item is None:
            item = Text()

        item.x = self.x
        item.y = self.y
        item.text = self.text
        item.angle = self.angle

        item.font = self.font.copy()

        item.baseline = self.baseline
        item.anchor = self.anchor

        item = super().copy(item)

        return item

    def construct(self, **kwargs):
        if self.font is None:
            self.active = False

        if not self.active:
            return ''

        if self.angle != 0:
            transform = "translate(%s, %s) rotate(%s)" % (self.x, self.y, self.angle)
            x = 0
            y = 0
        else:
            transform = None
            x = self.x
            y = self.y

        parameters = {'x': x,
                      'y': y,
                      'font-family': self.font.family,
                      'font-size': self.font.size,
                      'font-weight': self.font.weight,
                      'dominant-baseline': self._baseline,
                      'text-anchor': self._anchor,
                      'xml:space': 'preserve',
                      'transform': transform}

        entries = super().construct(parameters)

        row = '<text %s>%s</text>' % (entries, str(self.text))

        return row


class Font:
    def __init__(self, family: str, size: int, weight: str):
        # Searches Working Directory for font path
        # path is parent/fonts/family/weight.ttf
        # Currently only formatted for truetype fonts
        path = P.cwd().parent
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
        font = Font(self.family, self.size, self.weight)

        return font

    def getTextWidth(self, text):
        total = 0
        for character in text:
            if ord(character) in self.cmap and self.cmap[ord(character)] in self.glyph_set:
                total += self.glyph_set[self.cmap[ord(character)]].width
            else:
                total += self.glyph_set['.notdef'].width
        total = total * float(self.size) / self.units_per_em
        return total
