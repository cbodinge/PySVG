from .Text import Text
from ..Draw import Rect
from ..SVG import Section


class TextBox(Section):
    def __init__(self, text: Text, alignment=(1, 1), dL=3, dB=3, dR=3, dT=3, **kwargs):
        super().__init__(**kwargs)

        self.background = Rect(active=False)
        self.addChild(self.background)

        self._text = text.copy()
        self.addChild(self._text)

        # Margins to aid in alignment
        self.dL = dL
        self.dB = dB
        self.dR = dR
        self.dT = dT

        self.alignment = alignment

    def _horizontal(self):
        t = self._text
        x = self.alignment[0]

        if x == 0:
            t.x = self.dL
            t.anchor = 'start'

        elif x == 1:
            t.x = '50%'
            t.anchor = 'middle'

        elif x == 2:
            t.x = self.w - self.dR
            t.anchor = 'end'

    def _vertical(self):
        t = self._text
        y = self.alignment[1]

        if y == 0:
            t.y = self.dT
            t.baseline = 'hanging'

        elif y == 1:
            t.y = '50%'
            t.baseline = 'central'

        elif y == 2:
            t.y = self.h - self.dB
            t.baseline = 'auto'

    def set(self):
        self._horizontal()
        self._vertical()

    @property
    def text(self):
        return self._text.text

    @text.setter
    def text(self, text: str):
        self._text.text = text

    @property
    def textColor(self):
        return self._text.fill

    @textColor.setter
    def textColor(self, val: tuple[int, int, int]):
        self._text.fill = val

    @property
    def textOpacity(self):
        return self._text.fill_opacity

    @textOpacity.setter
    def textOpacity(self, val: float):
        self._text.fill_opacity = val

    @property
    def fill(self):
        return self.background.fill

    @fill.setter
    def fill(self, val: tuple[int, int, int]):
        self.background.fill = val

    @property
    def fill_opacity(self):
        return self.background.fill_opacity

    @fill_opacity.setter
    def fill_opacity(self, val: float):
        self.background.fill_opacity = val

    @property
    def stroke(self):
        return self.background.stroke

    @stroke.setter
    def stroke(self, val: tuple[int, int, int]):
        self.background.stroke = val

    @property
    def stroke_opacity(self):
        return self.background.stroke_opacity

    @stroke_opacity.setter
    def stroke_opacity(self, val: float):
        self.background.stroke_opacity = val

    @property
    def stroke_width(self):
        return self.background.stroke_width

    @stroke_width.setter
    def stroke_width(self, val: float):
        self.background.stroke_width = val
