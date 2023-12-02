from ..Text import Text
from ..SVG import Section
from ..Draw import Rect


class Paragraph(Section):
    def __init__(self, text: Text, w: float, h: float, x: float = 0, y: float = 0):
        super().__init__(x, y, w, h)

        self.linewidth = 0
        self.indention = 0
        self.text = text
        self.text.baseline = 'hanging'

        self.background = Rect(fill=(255, 255, 255), fill_opacity=1, active=False)
        self.addChild(self.background)

        self.fit = True
        self.lines = []

        self._get_lines()

    def _get_lines(self):
        t = self.text
        lines = []
        words = t.text.split(' ')
        wlens = [sum([self.text.font[ord(letter)] for letter in word]) * t.size / t.font.units_per_em for word in words]
        space = self.text.font[ord(' ')] * t.size / t.font.units_per_em

        s = 0
        beg = 0
        for i, word in enumerate(words):
            pos = s + space + wlens[i]
            if pos > self.w:
                lines.append(' '.join(words[beg:i]))
                beg = i
                s = 0
            elif pos == self.w:
                lines.append(' '.join(words[beg:i + 1]))
                beg = i + 1
                s = 0
            else:
                if i == len(words) - 1:
                    lines.append(' '.join(words[beg:]))
                s = pos

        self.lines = lines

    def set(self):
        if self.h == 0:
            # assign h based on linwidth and number of lines
            self.h = self.linewidth * len(self.lines)
        else:
            # assign linewidth based on h
            self.linewidth = self.h / len(self.lines)

        for i, line in enumerate(self.lines):
            t = self.text.copy()
            t.text = line
            t.x = 0
            t.y = i * self.linewidth

            self.addChild(t)

        return self.root
