from psvg import Rect, SVG, Text


class Table(SVG.SVG):
    def __init__(self):
        super().__init__(0, 0)
        self.rows = {}
        self.cols = {}
        self.boxes = {}
        self.text = Text.Text()

        self._check_row(0)
        self._check_col(0)

    class Column(SVG.SVG_g):
        def __init__(self):
            super().__init__(0, 0)
            self._width = 0
            self.background = Rect.Rect()
            self.add_child(self.background)
            self.custom = False

        @property
        def w(self):
            return self._width

        def set_w(self, width: float, overide=False):
            self._width = width
            if not overide:
                self.custom = True

        def set_sizes(self, x, h):
            self.x, self.y = x, 0
            self.background.w, self.background.h = self.w, h

    class Row(SVG.SVG_g):
        def __init__(self):
            super().__init__(0, 0)
            self.y = 0
            self._height = 0
            self.background = Rect.Rect()
            self.add_child(self.background)
            self.custom = False

        @property
        def h(self):
            return self._height

        def set_h(self, height: float, overide=False):
            self._height = height
            if not overide:
                self.custom = True

        def set_sizes(self, y, w):
            self.x, self.y = 0, y
            self.background.w, self.background.h = w, self.h

    class Box(SVG.SVG):
        def __init__(self, text: Text.Text):
            super().__init__(0, 0)
            self.row = None
            self.col = None

            self.background = Rect.Rect()
            self.add_child(self.background)

            self.text = text
            self.add_child(self.text)

        def construct(self):
            self.size = (self.col.w, self.row.h)
            svg = ['<g transform="matrix(1,0,0,1,%s,%s)"> ' % (self.col.x, self.row.y), super().construct(), '</g>']
            svg = '\n'.join(svg)

            return svg

    def _check_row(self, row):
        if row not in self.rows.keys():
            self.rows[row] = self.Row()
            self.add_child(self.rows[row])
            self.boxes[row] = {}

    def _check_col(self, col):
        if col not in self.cols.keys():
            self.cols[col] = self.Column()
            self.add_child(self.cols[col])

    def add_item(self, row, col, val=None):
        max_rows = max(list(self.rows.keys()) + [row])
        max_cols = max(list(self.cols.keys()) + [col])

        for i in range(max_rows + 1):
            self._check_row(i)

        for i in range(max_cols + 1):
            self._check_col(i)

        new_box = self.Box(self.get_text())
        self.add_section(new_box, 0, 0)
        if val is not None:
            new_box.text.text = str(val)

        new_box.row = self.rows[row]
        new_box.col = self.cols[col]
        self.boxes[row][col] = new_box

    def _set_cols(self):
        w, h = self.size
        cw = 0
        dflt = []

        for col in self.cols.values():
            if col.custom:
                cw = cw + col.w
            else:
                dflt.append(col)

        leftovers = w - cw
        dw = 0
        if leftovers > 0 and len(dflt) > 0:
            dw = leftovers / (len(dflt))
        for col in dflt:
            col.set_w(dw, True)

        x = 0
        for col in self.cols.values():
            col.set_sizes(x, h)
            x = x + col.w

    def _set_rows(self):
        w, h = self.size
        ch = 0
        dflt = []

        for row in self.rows.values():
            if row.custom:
                ch = ch + row.h
            else:
                dflt.append(row)

        leftovers = h - ch
        dh = 0
        if leftovers > 0 and len(dflt) > 0:
            dh = leftovers / len(dflt)
        for row in dflt:
            row.set_h(dh, True)

        y = 0
        for row in self.rows.values():
            row.set_sizes(y, w)
            y = y + row.h

    def get_text(self):
        text = Text.Text()
        return text

    def construct(self):
        self._set_rows()
        self._set_cols()
        svg = super().construct()

        return svg
