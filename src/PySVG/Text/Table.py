from .Text import Text
from ..Draw import Rect
from ..SVG import SVG, Section


class Table(SVG):
    def __init__(self, text):
        super().__init__(0, 0)
        self.rows = []
        self.cols = []
        self.boxes = {}
        self.text = text

        self._check_row(0)
        self._check_col(0)

    def _check_row(self, row):
        n = len(self.rows)
        if row < n:
            return

        for i in range(n, row + 1):
            r = Row(self)
            self.rows.append(r)

    def _check_col(self, col):
        n = len(self.cols)
        if col < n:
            return

        for i in range(n, col + 1):
            c = Column(self)
            self.cols.append(c)

    def add_item(self, row, col, val=None):
        max_rows = max(list(range(len(self.rows))) + [row])
        max_cols = max(list(range(len(self.cols))) + [col])

        for i in range(max_rows + 1):
            self._check_row(i)

        for i in range(max_cols + 1):
            self._check_col(i)

        new_box = TextBox(self.text.copy(), self.rows[row], self.cols[col])

        if val is not None:
            new_box.text.text = str(val)

        self.boxes[row, col] = new_box

    def set_sizes(self):
        self._set_rows()
        self._set_cols()

    def _set_cols(self):
        w, h = self.size
        cw = 0
        dflt = []

        for col in self.cols:
            if col.lock:
                cw = cw + col.w
            else:
                dflt.append(col)

        leftovers = w - cw
        dw = 0
        if leftovers > 0 and len(dflt) > 0:
            dw = leftovers / (len(dflt))
        for col in dflt:
            col.w = dw
            col.lock = False

        x = 0
        for col in self.cols:
            col.x = x
            col.h = h
            x = x + col.w

    def _set_rows(self):
        w, h = self.size
        ch = 0
        dflt = []

        for row in self.rows:
            if row.lock:
                ch = ch + row.h
            else:
                dflt.append(row)

        if not dflt:
            h = sum([row.h for row in self.rows])
            self.size = (w, h)

        leftovers = h - ch
        dh = 0
        if leftovers > 0 and len(dflt) > 0:
            dh = leftovers / len(dflt)

        for row in dflt:
            row.set_h(dh)
            row.lock = False

        y = 0
        for row in self.rows:
            row.y = y
            row.w = w
            y = y + row.h

    def construct(self):
        self.set_sizes()

        for col in self.cols:
            self.add_child(col)

        for row in self.rows:
            self.add_child(row)

        for box in self.boxes.values():
            self.add_child(box)

        svg = super().construct()

        return svg


class Row(Rect):
    def __init__(self, parent: SVG, h: float = 0):
        super().__init__()
        w, _ = parent.size
        self.x = 0
        self.y = 0
        self.w = w
        self.h = h

        self.lock = False

    def set_h(self, height):
        self.h = height
        self.lock = True


class Column(Rect):
    def __init__(self, parent: SVG, w: float = 0):
        super().__init__()
        _, h = parent.size
        self.x = 0
        self.y = 0
        self.w = w
        self.h = h

        self.lock = False

    def set_w(self, width):
        self.w = width
        self.lock = True


class TextBox(Section):
    def __init__(self, text: Text, row, col):
        super().__init__(0, 0)
        self.row, self.col = row, col

        self.rect = Rect()
        self.rect.active = False

        self.text = text

        self.margin = 0.03

        self.alignment = self.center

    def center(self):
        w = self.col.w
        self.text.x = w / 2
        self.text.anchor = 'middle'
        self.middle()

    def left(self):
        w = self.col.w
        self.text.x = self.margin * w
        self.text.anchor = 'start'
        self.middle()

    def right(self):
        w = self.col.w
        self.text.x = w - self.margin * w
        self.text.anchor = 'end'
        self.middle()

    def middle(self):
        h = self.row.h
        self.text.y = h / 2
        self.text.baseline = 'central'

    def _set(self):
        self.alignment()
        self.rect.w = self.col.w
        self.rect.h = self.row.h

        self.x = self.col.x
        self.y = self.row.y

    def construct(self):
        self._set()
        self.add_child(self.rect)
        self.add_child(self.text)

        return super().construct()
