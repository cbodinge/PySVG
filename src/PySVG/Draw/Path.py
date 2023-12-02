from .Base import Base


class Path(Base):
    """
    Repressents a generic version of the path element of an SVG.

    Path elements are used to draw curves and shapes
    freely based on defined curve behavior and coordinates on which to draw. Subclass of `Base.Base`.
    """

    def __init__(self):
        super().__init__(name='path')
        self.points = []
        self.type = 'path'

    def _validate(self):
        super(Path, self)._validate()

        # path #########################################################################################################
        if self.points is not None:
            d = ', '.join([' '.join([str(p) for p in point if str(p) != '']) for point in self.points])
            self.valid['d'] = f'd="{d}"'