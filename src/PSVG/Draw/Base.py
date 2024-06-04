from ..Data_Structures import Node


# noinspection PyBroadException
class Base(Node):
    """
    Abstract Class

    Sets the parameters shared by all drawn objects.

    Currently, these are as follows:
    - fill: an (r, g, b) tuple that sets the fill color of the object
    - fill_opacity: a float value between 0 and 1 that sets the opacity of the object
    - stroke: an (r, g, b) tuple that sets the color of the object border
    - stroke_opacity: a float value between 0 and 1 that sets the opacity of the object border
    - stroke_width: a float that sets the width of the object border
    - stroke_dasharray: a list of integers that sets the design of the object border dashes if desired

    Any parameter not set will be absent from the svg definition.
    """

    def __init__(self, name, fill=None, fill_opacity=None, stroke=None, stroke_width=None, stroke_opacity=None,
                 stroke_dasharray=None, active=True):
        super().__init__(name)
        self.type = ''

        self.fill = fill
        self.fill_opacity = fill_opacity

        self.stroke = stroke
        self.stroke_width = stroke_width
        self.stroke_opacity = stroke_opacity
        self.stroke_dasharray = stroke_dasharray

        self.valid = {}

        self.active = active

    def __str__(self):
        self._validate()
        s = ' '.join([i for i in self.valid.values() if i is not None])
        return f'<{self.type} {s}/>'

    @staticmethod
    def _color2hex(color: tuple[int, int, int]):
        """
        Converts an RGB color tuple to a hex string
        :param color: (r, g, b) tuple that defines the color
        :return: hex color string
        """
        try:
            red, green, blue = [f'{i:0{2}x}' for i in color]
            return f'#{red}{green}{blue}'
        except:
            return None

    @staticmethod
    def _get_string_value(val, var):
        """
        returns the appropriate value for the given svg attribute
        :param val: value of the svg attribute
        :param var: name of the svg attribute
        :return: formatted attribute string
        """
        try:
            if val is not None:
                val = str(val)
                return f'{var}="{val}"'
        except:
            return None

    def _validate(self):
        """
        Validates each svg attribute
        """
        # Fill #########################################################################################################
        if self.fill is not None:
            color = self._color2hex(self.fill)
            if color is not None:
                self.valid['fill'] = f'fill="{color}"'

        # Fill Opacity #################################################################################################
        val = self.fill_opacity
        try:
            if val < 0:
                val = 0
            if val > 1:
                val = 1

            self.valid['fill opacity'] = f'fill-opacity="{val}"'
        except:
            pass

        # Stroke #######################################################################################################
        if self.stroke is not None:
            color = self._color2hex(self.stroke)
            if color is not None:
                self.valid['stroke'] = f'stroke="{color}"'

        # Stroke Width #################################################################################################
        if self.stroke_width is not None:
            try:
                self.valid['stroke width'] = f'stroke-width="{self.stroke_width}"'
            except:
                pass

        # Stroke Opacity ###############################################################################################
        val = self.stroke_opacity
        try:
            if val < 0:
                val = 0
            if val > 1:
                val = 1

            self.valid['stroke opacity'] = f'stroke-opacity="{val}"'
        except:
            pass

        # Stroke Dasharray #############################################################################################
        val = self.stroke_dasharray
        if val is not None:
            try:
                dashes = ' '.join([str(i) for i in val])
                self.valid['stroke dasharray'] = f'stroke-dasharray="{dashes}"'
            except:
                pass

    def construct(self, depth):
        """
        Constructs the svg definition
        :param depth: current depth of this node in the svg tree
        :return: String containing the svg definition for this object
        """
        if self.active is False:
            return ''

        self._validate()
        s = ' '.join([i for i in self.valid.values() if i is not None])
        return f'{"   " * depth}<{self.type} {s}/>'

    def copy(self, item: 'Base' = None):
        """
        Creates a copy of this node either by creating a new object
        or by adjusting the values of the object referenced by item

        :param item: reference to an existing node
        :return: a node with the same attributes as this node
        """
        item = Base('') if item is None else item

        item.name = self.name
        item.fill = self.fill
        item.fill_opacity = self.fill_opacity
        item.stroke = self.stroke
        item.stroke_width = self.stroke_width
        item.stroke_opacity = self.stroke_opacity
        item.stroke_dasharray = self.stroke_dasharray
        item.active = self.active

        return item
