from ..Draw.Base import Base


class Text(Base):
    # todo: add documentation
    def __init__(self, font, text='', size=10, x=0, y=0, angle=0, baseline=None, anchor=None, **kwargs):
        super().__init__('text', **kwargs)
        self.text = text
        self.x = x
        self.y = y
        self.angle = angle
        self.font = font
        self.size = size

        self.type = 'text'

        self.baseline = baseline
        # options
        # auto, text-bottom, alphabetic, ideographic, middle, central, mathematical, hanging, text-top

        self.anchor = anchor
        # options
        # 'start', 'middle', 'end'

    def _validate(self):
        super(Text, self)._validate()
        s = super(Text, self)._get_string_value

        if self.angle != 0:
            # x ########################################################################################################
            self.valid['x'] = s(0, 'x')

            # y ########################################################################################################
            self.valid['y'] = s(0, 'y')

            # angle ####################################################################################################
            self.valid['transform'] = f'transform = "translate({self.x}, {self.y}) rotate({self.angle})"'
        else:
            # x ########################################################################################################
            self.valid['x'] = s(self.x, 'x')

            # y ########################################################################################################
            self.valid['y'] = s(self.y, 'y')

        # font size ####################################################################################################
        self.valid['size'] = s(self.size, 'font-size')

        # font weight ##################################################################################################
        self.valid['weight'] = s(self.font.weight, 'font-weight')

        # font family ##################################################################################################
        self.valid['family'] = s(self.font.family, 'font-family')

        # baseline #####################################################################################################
        self.valid['dominant baseline'] = s(self.baseline, 'dominant-baseline')

        # anchor #######################################################################################################
        self.valid['text-anchor'] = s(self.anchor, 'text-anchor')

        # preserve spaces ##############################################################################################
        self.valid['xml:space'] = s('preserve', 'xml:space')

    def construct(self, depth):
        if self.active is False:
            return ''

        tab = '   ' * depth
        self._validate()
        s = ' '.join([i for i in self.valid.values() if i is not None])
        return f'{tab}<text {s}>{self.text}</text>'

    def copy(self, item: 'Text' = None):
        item = super().copy(Text(self.font)) if item is None else super().copy(item)

        item.font = self.font
        item.text = self.text
        item.size = self.size
        item.x = self.x
        item.y = self.y
        item.angle = self.angle
        item.baseline = self.baseline
        item.anchor = self.anchor

        return item

    @property
    def width(self):
        return sum([self.font[ord(letter)] for letter in self.text]) * self.font.unit_per_em
