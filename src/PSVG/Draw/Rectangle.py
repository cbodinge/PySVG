from .Base import Base


class Rect(Base):
    """
    Concrete Implementation of `Draw.Base`

    Represents a rectangle SVG element.
    """

    def __init__(self, x=0, y=0, w='100%', h='100%', rx=None, ry=None, **kwargs):
        """
        :param x: x coordinate of the left, bottom coordinate of the rectangle
        :param y: y coordinate of the left, bottom coordinate of the rectangle
        :param w: Width of the rectangle
        :param h: Height of the rectangle
        :param rx: changes the horizontal rounding of the rectangle edges
        :param ry: changes the vertical rounding of the rectangle edges

        All location/size parameters Can be pixels, percent, or any of the supported units
        (see `Units Documentation <https://developer.mozilla.org/en-US/docs/Web/CSS/length-percentage>`_
        for details on what units are supported). Default is pixel values.
        """
        super().__init__(name='Rect', **kwargs)
        self.type = 'rect'

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.rx = rx
        self.ry = ry

    def _validate(self):
        super(Rect, self)._validate()
        s = super(Rect, self)._get_string_value

        # x ############################################################################################################
        self.valid['x'] = s(self.x, 'x')

        # y ############################################################################################################
        self.valid['y'] = s(self.y, 'y')

        # w ############################################################################################################
        self.valid['w'] = s(self.w, 'width')

        # h ############################################################################################################
        self.valid['h'] = s(self.h, 'height')

        # rx ###########################################################################################################
        self.valid['rx'] = s(self.rx, 'rx')

        # ry ###########################################################################################################
        self.valid['ry'] = s(self.ry, 'ry')

    def copy(self, item: 'Rect' = None):
        item = super().copy(Rect()) if item is None else super().copy(item)

        item.x = self.x
        item.y = self.y
        item.w = self.w
        item.h = self.h
        item.rx = self.rx
        item.ry = self.ry

        return item
