from Paths import Path


class Rect(Path):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.w = '100%'
        self.h = '100%'

        self.rx = None
        self.ry = None

        self.fill_opacity = 0

    def copy(self, item=None):
        if item is None:
            item = Rect()

        item.x = self.x
        item.y = self.y
        item.w = self.w
        item.h = self.h

        item.rx = self.rx
        item.ry = self.ry

        item = super().copy(item)

        return item

    def construct(self, **kwargs):
        if not self.active:
            return ''

        parameters = {'x': self.x,
                      'y': self.y,
                      'rx': self.rx,
                      'ry': self.ry,
                      'width': self.w,
                      'height': self.h}

        entries = super().construct(parameters)

        row = '<rect %s />' % (entries,)

        return row


class Circle(Path):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.r = 0

    def copy(self, item=None):
        if item is None:
            item = Rect()

        item.x = self.x
        item.y = self.y
        item.r = self.r

        item = super().copy(item)

        return item

    def construct(self, **kwargs):
        parameters = {'cx': self.x,
                      'cy': self.y,
                      'r': self.r}

        entries = super().construct(parameters)

        row = '<circle %s />' % (entries,)

        return row


class Generic_Path(Path):
    def __init__(self):
        super().__init__()
        self.points = []

    def copy(self, item=None):
        if item is None:
            item = Generic_Path()

        item.points = self.points

        item = super().copy(item)

        return item

    def construct(self, **kwargs):
        entries = super().construct()

        points = ', '.join([' '.join([str(p) for p in point if str(p) != '']) for point in self.points])

        row = '<path d="%s"' % (points,)

        row = row + ' ' + entries + '/>'

        return row
