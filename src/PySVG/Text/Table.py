from .Text import Text
from ..Draw import Rect
from ..SVG import SVG, Section


class Table(SVG):
    def __init__(self, text, data: list[list[str]], w=0, h=0):
        super().__init__(w, h)
        self.boxes = {(i, j): data[i][j] for i in range(len(data)) for j in range(len(data[0]))}
        self.text = text
        self.rows = [0 for _ in range(len(data))]
        self.cols = [0 for _ in range(len(data[0]))]

        self._rows = [0 for _ in self.r_rng]
        self._cols = [0 for _ in self.c_rng]

        self._rr = [Rect(active=False) for _ in self.r_rng]
        self._cr = [Rect(active=False) for _ in self.c_rng]

        _ = [self.add_child(self._rr[i]) for i in self.r_rng]
        _ = [self.add_child(self._cr[i]) for i in self.c_rng]

        self._from_data(data)

        self.background = Rect()
        self.background.active = False

    @property
    def r_rng(self):
        return range(len(self.rows))

    @property
    def c_rng(self):
        return range(len(self.cols))

    def _from_data(self, data):
        for row, lst in enumerate(data):
            for col, el in enumerate(lst):
                self.add_box(row, col, el)

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

        self.boxes[row, col] = TextBox(text)
        self.add_child(self.boxes[row, col].root)

    def set_row_height(self, height):
        for i in self.r_rng:
            self._rows[i] = height

        self.h = height * len(self.rows)

    def set_col_width(self, width):
        for i in self.c_rng:
            self._cols[i] = width

        self.w = width * len(self.rows)

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

    def weighted_col_width(self, total_w: float, weights: list[float]):
        """
        Given the desired width and weights, computes the column width for each column.

        :param total_w: number representing the desired width of the table
        :param weights: list of percentages that define column widths
        """
        self._cols = [total_w * weights[i] for i in self.c_rng]
        self.w = total_w

    def weighted_row_width(self, total_h: float, weights: list[float]):
        """
        Given the desired height and weights, computes the row height for each row.

        :param total_h: number representing the desired height of the table
        :param weights: list of percentages that define row heights
        """
        self._rows = [total_h * weights[i] for i in self.r_rng]
        self.h = total_h

    def set_sizes(self):
        self.w = sum(self._cols)
        self.h = sum(self._rows)
        y = 0
        for row in self.r_rng:
            h = self._rows[row]
            x = 0
            rect = self._rr[row]
            rect.y = y
            rect.h = h
            rect.w = self.w
            for col in self.c_rng:
                w = self._cols[col]

                if y == 0:
                    rect = self._cr[col]
                    rect.x = x
                    rect.h = self.h
                    rect.w = w

                box = self.boxes[row, col]
                box.x = x
                box.y = y
                box.w = w
                box.h = h

                x += w
            y += h

    def set_box_text(self, row: int, col: int, to_copy: Text):
        box = self.boxes[row, col]
        text = box.text.text
        box.text = to_copy.copy()
        box.text.text = text

    def set_row_text(self, to_copy: Text, row: int):
        for i in self.c_rng:
            self.set_box_text(row, i, to_copy)

    def set_col_text(self, to_copy: Text, col: int):
        for i in self.c_rng:
            self.set_box_text(i, col, to_copy)

    def set_box_color(self, row: int, col: int, color: tuple[int, int, int], opacity: float):
        box = self.boxes[row, col].rect
        box.active = True
        box.fill = color
        box.fill_opacity = opacity

    def set_rect_color(self, rect: Rect, color: tuple[int, int, int], opacity: float):
        rect.active = True
        rect.fill = color
        rect.fill_opacity = opacity

    def set_row_color(self, row: int, color: tuple[int, int, int], opacity: float):
        self.set_rect_color(self._rr[row], color, opacity)

    def set_col_color(self, col: int, color: tuple[int, int, int], opacity: float):
        self.set_rect_color(self._cr[col], color, opacity)

    def set(self):
        self.set_sizes()
        for box in self.boxes.values():
            box.set()


class TextBox(Section):
    def __init__(self, text: Text):
        super().__init__()

        self.rect = Rect(x=0, y=0, w='100%', h='100%')
        self.rect.active = False

        self.text = text

        self.margin = 0.03

        self.alignment = self.right

    def _center(self):
        self.text.x = self.w / 2
        self.text.anchor = 'middle'
        self.middle()

    def left(self):
        self.text.x = self.margin * self.w
        self.text.anchor = 'start'
        self.middle()

    def right(self):
        self.text.x = self.w - self.margin * self.w
        self.text.anchor = 'end'
        self.middle()

    def middle(self):
        self.text.y = self.h / 2
        self.text.baseline = 'central'

    def set(self):
        self.alignment()
        self.middle()
        self.addChild(self.rect)
        self.addChild(self.text)
