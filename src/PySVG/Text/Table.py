from .Text import Text
from ..Draw import Rect
from ..SVG import SVG, Section


class Table(SVG):
    def __init__(self, text):
        super().__init__(0, 0)
        self.rows = {}
        self.cols = {}
        self.boxes = {}
        self.text = text

        self.background = Rect()
        self.background.active = False

    def add_box(self, row, col, value):
        """
        Adds a text box to the table at the intersection of row and column.
        If something exists there already this will overwrite it.

        :param row: Integer represent the row to put the box in
        :param col: Integer representing the column to but the box in
        :param value: The text value of the text box

        """
        text = self.text.copy()
        text.text = str(value)

        self.add_row(row)
        self.add_col(col)

        box = TextBox(text, self.rows[row], self.cols[col])
        self.boxes[row, col] = box

    def add_row(self, row_index: int):
        if row_index not in self.rows.keys():
            row = Row(self, row_index)
            self.rows[row_index] = row

    def add_col(self, col_index: int):
        if col_index not in self.cols.keys():
            col = Column(self, col_index)
            self.cols[col_index] = col

    def set_row_height(self, height):
        for row in self.rows.values():
            row.h = height

    def set_col_width(self, width):
        for col in self.cols.values():
            col.w = width

    def even_row_height(self, total_h):
        """
        Given the desired height, computes the row height for each row assuming all rows will have the same row height.

        :param total_h: number representing the desired height of the table
        """
        max_row = len(self.rows)
        h = total_h / max_row
        self.set_row_height(h)

    def even_col_width(self, total_w):
        """
        Given the desired width, computes the column width for each column
        assuming all columns will have the same column width.

        :param total_w: number representing the desired width of the table
        """
        max_col = len(self.cols)
        w = total_w / max_col
        self.set_col_width(w)

    def weighted_col_width(self, total_w, weights):
        """
        Given the desired width and weights, computes the column width for each column.

        :param total_w: number representing the desired width of the table
        """
        max_col = len(self.cols)
        i = 0
        for col in self.cols.values():
            col.w = total_w * weights[i]
            i += 1

    def weighted_row_width(self, total_h, weights):
        """
        Given the desired height and weights, computes the row height for each row.

        :param total_h: number representing the desired height of the table
        """
        max_col = len(self.rows)
        i = 0
        for row in self.rows.values():
            row.h = total_h * weights[i]
            i += 1

    def set_sizes(self):
        self._rows()
        self._cols()
        self._boxes()

        w = sum([col.w for col in self.cols.values()])
        h = sum([row.h for row in self.rows.values()])

        self.size = (w, h)

    def _rows(self):
        rows = list(self.rows.keys())
        rows.sort()
        y = 0
        for i in rows:
            row = self.rows[i]
            row.w = self.w
            row.y = y
            y += row.h

    def _cols(self):
        cols = list(self.cols.keys())
        cols.sort()
        x = 0
        for i in cols:
            col = self.cols[i]
            col.h = self.h
            col.x = x
            x += col.w

    def _boxes(self):
        for box in self.boxes.values():
            box.x = box.col.x
            box.y = box.row.y

    def construct(self):
        for row in self.rows.values():
            self.add_child(row)

        for col in self.cols.values():
            self.add_child(col)

        for box in self.boxes.values():
            self.add_child(box)

        return super().construct()


class Row(Rect):
    def __init__(self, parent: Table, index: int, h: float = 0):
        super().__init__()
        w, _ = parent.size
        self._parent = parent
        self._index = index

        self.x = 0
        self.y = 0
        self.w = w
        self.h = h

    def _children(self):
        cols = list(self._parent.cols.keys())
        row = self._index

        return [self._parent.boxes[row, col] for col in cols]

    def text_color(self, color: tuple[int, int, int]):
        """
        Sets the text color for all boxes in this column.

        :param color: tuple of rgb values representing the color of the text
        """
        for child in self._children():
            child.text.fill = color


class Column(Rect):
    align_center = 0
    align_left = 1
    align_right = 2

    def __init__(self, parent: Table, index: int, w: float = 0):
        super().__init__()
        _, h = parent.size
        self._parent = parent
        self._index = index

        self.x = 0
        self.y = 0
        self.w = w
        self.h = h

    def _children(self):
        rows = range(len(self._parent.rows))
        col = self._index

        return [self._parent.boxes[row, col] for row in rows]

    def align_text(self, alignment: int):
        """
        Sets the test alignment for the column.

        :param alignment: integer representing the type of alignment to do for the entire column.
        This can be overridden later.
            (see Column.align_center, Column.align_left, Column.align_right)
        """

        def alignment_rules(box):
            if alignment == self.align_left:
                box.left()
            elif alignment == self.align_center:
                box.center()
            elif alignment == self.align_right:
                box.right()

        for child in self._children():
            alignment_rules(child)

    def text_color(self, color: tuple[int, int, int]):
        """
        Sets the text color for all boxes in this column.

        :param color: tuple of rgb values representing the color of the text
        """
        for child in self._children():
            child.text.fill = color

    def construct(self, **kwargs):
        return super().construct()


class TextBox(Section):
    def __init__(self, text: Text, row, col):
        super().__init__(0, 0)
        self.row, self.col = row, col

        self.rect = Rect()
        self.rect.active = False

        self.text = text

        self.margin = 0.03

        self.alignment = self.center

    def _center(self):
        w = self.col.w
        self.text.x = w / 2
        self.text.anchor = 'middle'
        self.middle()

    def _left(self):
        w = self.col.w
        self.text.x = self.margin * w
        self.text.anchor = 'start'
        self.middle()

    def _right(self):
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

    def left(self):
        self.alignment = self._left

    def right(self):
        self.alignment = self._right

    def center(self):
        self.alignment = self._center
        return

    def construct(self):
        self._set()

        self.add_child(self.rect)
        self.add_child(self.text)

        return super().construct()
