from .Base import Base


class Path(Base):
    """
    Concrete Implementation of `Draw.Base`

    Represents a generic version of the path element of an SVG.

    Path elements are used to draw curves and shapes
    freely based on defined curve behavior and coordinates on which to draw.
    """

    def __init__(self, points=None, **kwargs):
        """
        :param points: a tuple of the form (command, x, y) where command is one of the following:
        'M': move to the point (x, y)
        'L': draw a line from the current location to (x, y)
        'V': draw a vertical line from the current location to (y)
        'H': draw a horizontal line from the current location to (x)
        'C': use the following points to draw a Cubic Bézier Curve

        see `Paths Documentation <https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths>`_
        for details on what path operations are supported
        """
        super().__init__(name='path', **kwargs)
        self.points = [] if points is None else points
        self.type = 'path'

    def _validate(self):
        super(Path, self)._validate()

        # path #########################################################################################################
        if self.points is not None:
            d = ', '.join([' '.join([str(p) for p in point if str(p) != '']) for point in self.points])
            self.valid['d'] = f'd="{d}"'

    def copy(self, item: 'Path' = None):
        item = super().copy(Path()) if item is None else super().copy(item)

        item.points = self.points

        return item
