from psvg.Text import Text
from psvg.Rect import Rect
from copy import deepcopy


class Paragraph:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 1
        self.h = 1000
        self.linewidth = 0
        self.indention = 0
        self.text = Text()

        self._n = 0
        self.fit = True
        self.lines = []

        self.background = Rect()

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
        svg = ['<g transform="matrix(1,0,0,1,%s,%s)"> ' % (self.x, self.y),
               '<svg width="%s" height="%s" xmlns="http://www.w3.org/2000/svg">' % (self.w, self.h),
               self.background.construct()]

        i = .5
        for line in self.lines:
            text = deepcopy(self.text)
            text.y = i * self.linewidth
            text.x = 0
            text.text = line
            svg.append(text.construct())
            i += 1

        end = ['</svg>', '</g>']

        svg = svg + end

        return '\n'.join(svg)
