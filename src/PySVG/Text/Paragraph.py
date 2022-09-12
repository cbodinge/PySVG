from ..Text import Text
from ..SVG import Section


class Paragraph(Section):
    def __init__(self, x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.w = 1
        self.h = 1000

        self.linewidth = 0
        self.indention = 0
        self.text = Text()

        self._n = 0
        self.fit = True
        self.lines = []

    def _get_lines(self):
        words = self.text.text.split(' ')
        lines = []
        t = ' '

        while words:
            q = []
            line = ''
            while words:
                word = words.pop(0)
                if word != '\n':
                    line = self.indention * t + ' '.join(q) + ' ' + word
                    x = self.text.font.getTextWidth(line)
                    test = x < self.w
                    if test:
                        q.append(word)
                    else:
                        line = self.indention * t + ' '.join(q)
                        words.insert(0, word)
                        break
                else:
                    line = self.indention * t + ' '.join(q)
                    break

            lines.append(line)
            self._n = len(lines)

        return lines

    def makefit(self):
        self.lines = self._get_lines()
        self.h = self.linewidth * self._n

    def construct(self):
        self.makefit()

        i = .5
        for line in self.lines:
            text = self.text.copy()
            text.y = i * self.linewidth
            text.x = 0
            text.text = line
            self.add_child(text)
            i += 1

        return super().construct()
