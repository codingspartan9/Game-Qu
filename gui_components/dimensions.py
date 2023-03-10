class Dimensions:
    """ Gives left_edge, top_edge, height, length and then using those number it provides
        right_edge, bottom_edge, horizontal_midpoint, and vertical_midpoint"""

    left_edge = 0
    top_edge = 0
    length = 0
    height = 0

    def __init__(self, left_edge, top_edge, length, height):
        """Initializes all the attributes of the class with the numbers provided (calls self.number_set_dimensions())"""

        self.number_set_dimensions(left_edge, top_edge, length, height)

    @property
    def right_edge(self):
        """The left_edge + length is what constitutes the object's right_edge"""

        return self.left_edge + self.length

    @property
    def bottom_edge(self):
        """The top_edge + height is what constitutes the object's bottom_edge"""

        return self.top_edge + self.height

    @property
    def horizontal_midpoint(self):
        """The left_edge + length / 2 is what constitutes the object's horizontal_midpoint"""

        return self.left_edge + self.length / 2

    @property
    def vertical_midpoint(self):
        """The top_edge + height / 2 is what constitutes the object's vertical_midpoint"""

        return self.top_edge + self.height / 2

    def number_set_dimensions(self, left_edge, top_edge, length, height):
        """Sets the dimensions of this object (does the same thing as __init__)"""

        self.left_edge, self.top_edge, self.length, self.height = left_edge, top_edge, length, height

    def percentage_set_dimensions(self, percent_right, percent_down, percent_length, percent_height, horizontal_number, vertical_number):
        """ Sets the dimensions based on the values passed into this function

            :parameter percent_right: int; the percent it is to right (percentage of horizontal_number)
            :parameter percent_down: int; the percent it is down (percentage of horizontal_number)
            :parameter percent_length: int; the length (percentage of vertical_number)
            :parameter percent_height: int; the height (percentage of vertical_number)
            :parameter horizontal_number: int; what percent_right and percent_length are percentages of
            :parameter vertical_number: int; what percent_down and percent_height are percentages of

            :returns: None
        """

        self.left_edge = horizontal_number * percent_right / 100
        self.length = horizontal_number * percent_length / 100
        self.top_edge = vertical_number * percent_down / 100
        self.height = vertical_number * percent_height / 100