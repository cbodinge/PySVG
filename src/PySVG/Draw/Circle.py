from .Base import Base


class Circle(Base):
    def __init__(self, cx=0, cy=0, r=0, **kwargs):
        """
        :param x: x coordinate of the center of the circle.
        :param y: y coordinate of the center of the circle.
        :param r: radius of the circle.

        All location/size parameters Can be pixels, percent, or any of the supported units
        (see `Units Documentation <https://developer.mozilla.org/en-US/docs/Web/CSS/length-percentage>`_
        for details on what units are supported). Default is pixel values.
        """
        super().__init__(name='circle', **kwargs)

        self.cx = cx
        self.cy = cy
        self.r = r

        self.type = 'circle'

    def _validate(self):
        super(Circle, self)._validate()
        s = super(Circle, self)._get_string_value

        # cx ###########################################################################################################
        self.valid['cx'] = s(self.cx, 'cx')

        # cy ###########################################################################################################
        self.valid['cy'] = s(self.cy, 'cy')

        # r ############################################################################################################
        self.valid['r'] = s(self.r, 'r')

    def copy(self, item: 'Circle' = None):
        item = super().copy(Circle()) if item is None else super().copy(item)

        item.cx = self.cx
        item.cy = self.cy
        item.r = self.r

        return item
