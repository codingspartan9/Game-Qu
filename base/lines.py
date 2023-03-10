class Point:
    """Stores the x and y coordinates of point"""

    x_coordinate = 0
    y_coordinate = 0

    def __init__(self, x_coordinate, y_coordinate):
        """ Calls set_point(), so the x_coordinate and y_coordinate can be set

            :parameter x_coordinate: float; the value of the point's x coordinate
            :parameter y_coordinate: float; the value of the point's y coordinate

            :returns: None
        """

        self.set_coordinates(x_coordinate, y_coordinate)

    def set_coordinates(self, x_coordinate, y_coordinate):
        """ Sets the x_coordinate and y_coordinate can be set

            :parameter x_coordinate: float; the value of the point's x coordinate
            :parameter y_coordinate: float; the value of the point's y coordinate

            :returns: None
        """

        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate


class LineSegment:
    """Uses the equation y = mx + b where m is slope and b is y_intercept"""

    start_point = None
    end_point = None
    slope = None
    y_intercept = None

    def __init__(self, start_point, end_point):
        """ Sets the start and end point of the lines. It creates a very similar line if the x_coordinate of the start and end
            point have the same x_coordinate by adding a very small number to the end_point's x_coordinate. This makes
            finding where two lines collide alot easier. This function will call set_points()

            :parameter start_point: Point; a point on the line (different than end_point)
            :parameter end_point: Point; a point on the line (different than start_point)

            :returns: None
        """

        self.set_points(start_point, end_point)

    def set_points(self, start_point, end_point):
        """ Sets the start and end point of the lines. It creates a very similar line if the x_coordinate of the start and end
            point have the same x_coordinate by adding a very small number to the end_point's x_coordinate. This makes
            finding where two lines collide alot easier.

            :parameter start_point: Point; a point on the line (different than end_point)
            :parameter end_point: Point; a point on the line (different than start_point)

            :returns: None
        """

        self.start_point, self.end_point = start_point, end_point
        self.update_line_values()

    def update_line_values(self):
        """Updates the slope (m) and y_intercept (b) of the line through calculation. Uses the equation y = mx + b"""

        if self.start_point.x_coordinate == self.end_point.x_coordinate:
            self.end_point.x_coordinate += pow(10, -9)

        self.slope = (self.end_point.y_coordinate - self.start_point.y_coordinate) / (self.end_point.x_coordinate - self.start_point.x_coordinate)
        self.y_intercept = self.start_point.y_coordinate - self.slope * self.start_point.x_coordinate

    def get_y_coordinate(self, x_coordinate):
        """:returns: float; the y_coordinate at the x_coordinate"""

        return x_coordinate * self.slope + self.y_intercept

    def get_x_coordinate(self, y_coordinate):
        """:returns: float; the x_coordinate at the y_coordinate"""

        return (y_coordinate - self.y_intercept) / self.slope

    def contains_x_coordinate(self, x_coordinate):
        """:returns: bool; if the LineSegment contains the x_coordinate"""

        smaller_x_coordinate = self.start_point.x_coordinate if self.start_point.x_coordinate < self.end_point.x_coordinate else self.end_point.x_coordinate
        bigger_x_coordinate = self.start_point.x_coordinate if self.start_point.x_coordinate > self.end_point.x_coordinate else self.end_point.x_coordinate

        return x_coordinate >= smaller_x_coordinate and x_coordinate <= bigger_x_coordinate

    def contains_y_coordinate(self, y_coordinate):
        """:returns: bool; if the LineSegment contains the y_coordinate"""

        smaller_y_coordinate = self.start_point.y_coordinate if self.start_point.y_coordinate < self.end_point.y_coordinate else self.end_point.y_coordinate
        bigger_y_coordinate = self.start_point.y_coordinate if self.start_point.y_coordinate > self.end_point.y_coordinate else self.end_point.y_coordinate

        return y_coordinate >= smaller_y_coordinate and y_coordinate <= bigger_y_coordinate

    def contains_point(self, point):
        """:returns: bool; if the LineSegment contains the x_coordinate, y_coordinate, and point"""

        contains_coordinates = self.contains_x_coordinate(point.x_coordinate) and self.contains_y_coordinate(point.y_coordinate)
        correct_y_coordinate = point.y_coordinate == self.get_y_coordinate(point.x_coordinate)

        return contains_coordinates and correct_y_coordinate

    def slope_is_positive(self):
        """:returns: bool; if the slope is >= 0"""

        return self.slope >= 0
