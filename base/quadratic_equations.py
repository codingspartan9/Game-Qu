from game_qu.base.important_variables import SCREEN_HEIGHT
from game_qu.base.utility_functions import get_kwarg_item, solve_quadratic
from game_qu.base.velocity_calculator import VelocityCalculator


class QuadraticEquation:
    """A class that defines the necessary variables for a quadratic ax^2 + bx + c"""
    h = 0
    k = 0
    a = 0

    def set_variables(self, h, k, a):
        """ Sets the variables to the numbers to equation: a(x-h)^2 + k

            :parameter h: float; the first number of the vertex
            :parameter k: float; the second number of the vertex
            :parameter a: float; the number that goes before (x-h)^2

            :returns: None
        """

        self.h = h
        self.k = k
        self.a = a

    def get_number(self, x):
        """ Finds the number by plugging x into the equation ax^2 + bx + c

            :parameter x: float; the variable x that will be used to get the number

            :returns: float; the number that is gotten when x is plugged into the equation
        """

        return self.a * pow((x - self.h), 2) + self.k

    def points_set_variables(self, vertex, other_point):
        """ Sets the variables based on both points

            :parameter vertex: Point; the vertex of the quadratic equation
            :parameter other_point: Point; another point besides the vertex

            :returns: None
        """

        self.h = vertex.x_coordinate
        self.k = vertex.y_coordinate

        # Figured this out using algebra
        self.a = (other_point.y_coordinate - self.k) / pow((other_point.x_coordinate - self.h), 2)


class PhysicsEquation:
    """A class that uses common physics equations for initial_velocity, acceleration, and initial_distance"""

    acceleration = 0
    initial_velocity = 0
    initial_distance = 0

    def get_time_to_vertex(self):
        """ Gets the time it takes to reach the vertex knowing that the final initial_velocity is 0, so the time is -initial_velocity / acceleration

            :returns: float; the time to reach the vertex
        """

        return -self.initial_velocity / self.acceleration

    def set_acceleration_with_displacement(self, time, displacement):
        """ Sets the acceleration knowing that d = 1/2 * a * t^2 where d is displacement, a is acceleration, and t is time

            :parameter time: float; the amount of time that it should take to go that amount (displacement)
            :parameter displacement: float; the distance (up being positive and down being negative) that it should travel

            :returns: None
        """

        self.acceleration = (2 * displacement) / pow(time, 2)

    def set_acceleration_with_velocity(self, time, velocity_change):
        """Sets the acceleration knowing that vf = vi + at"""

        self.acceleration = velocity_change / time

    def set_all_variables(self, vertex, time, initial_distance):
        """ Sets all the variables; calls set_velocity and set_gravity_acceleration

            :parameter vertex: float; the highest/lowest point of the parabola
            :parameter time: float; the time it takes to get to the vertex/go the acceleration_distance
            :parameter acceleration_displacement: float; the distance (up being positive and down being negative) that the acceleration in that time
            :parameter initial_distance: float; the initial distance

            :returns: None
        """

        self.initial_distance = initial_distance

        # Gotten using math
        self.initial_velocity = (-2 * initial_distance + 2 * vertex) / time
        self.acceleration = 2 * (initial_distance - vertex) / pow(time, 2)

    def set_variables(self, **kwargs):
        """ Sets the variables to the number provided

            possible parameters:
                acceleration: float; the acceleration (can be positive or negative) | a in 1/2 * ax^2 + bx + c
                initial_velocity: float; the initial_velocity (can be positive or negative) | b in 1/2 * ax^2 + bx + c
                initial_distance: float; the starting point (can be positive or negative) | c in 1/2 * ax^2 + bx + c

            :returns: None
        """

        self.acceleration = get_kwarg_item(kwargs, "acceleration", self.acceleration)
        self.initial_velocity = get_kwarg_item(kwargs, "initial_velocity", self.initial_velocity)
        self.initial_distance = get_kwarg_item(kwargs, "initial_distance", self.initial_distance)

    def get_distance(self, time):
        """ Finds the number by plugging x into the equation 1/2 * at^2 + vt + d
            where a is acceleration, t is time, v is initial_velocity, and d is initial_distance

            :parameter time: float; the amount of time that has passed

            :returns: float; the number that is gotten when time is plugged into the equation
        """
        return 1 / 2 * self.acceleration * pow(time, 2) + self.initial_velocity * time + self.initial_distance

    def get_velocity_using_time(self, time):
        """ Uses the fact that the initial_velocity is equal to vi - at^2 where vi is the initial initial_velocity, a is acceleration, and t is time
            to find the initial_velocity

            :parameter time: float; the amount of time that the initial_velocity has been affected by acceleration

            :returns: float; the initial_velocity after affected by acceleration
        """

        return self.initial_velocity + self.acceleration * time

    def get_velocity_using_displacement(self, displacement):
        """ Uses the formula vf^2 = vi^2 + 2ax to find the initial_velocity
            where vf is final initial_velocity, vi is initial initial_velocity, a is acceleration, and x is displacement

            :parameter displacement: float; the amount that the ball has traveled (upwards is positive and downwards is negative)

            :returns: float; the final initial_velocity
        """

        final_velocity_squared = pow(self.initial_velocity, 2) + 2 * self.acceleration * displacement
        # Reduces the risk of a rounding error like -1*e^-15 would cause an imaginary number exception
        return pow(int(final_velocity_squared), 1 / 2)

    def get_vertex(self):
        """:returns: float; the vertex of this physics equation"""

        return self.get_distance(self.get_time_to_vertex())

    def get_times_to_point(self, distance):
        """ Finds the number by plugging in 'distance' into the equation 1/2 * at^2 + vt + d
            where a is acceleration, t is time, v is initial_velocity, and d is initial_distance

            :parameter distance: float; the distance that is wanted

            :returns: float[]; the times that the parabola is at that y coordinate
        """
        return solve_quadratic(1 / 2 * self.acceleration, self.initial_velocity, self.initial_distance - distance)

    def get_full_cycle_time(self):
        """:returns: float; the amount of time it takes the parabola to go from start_location -> start_location"""

        return self.get_time_to_vertex() * 2

    def __str__(self):
        return f"[{self.acceleration},{self.initial_velocity},{self.initial_distance},]"

    def __eq__(self, other):
        return (self.acceleration == other.acceleration and self.initial_velocity == other.initial_velocity and
                self.initial_distance == other.initial_distance)


class PhysicsPath(PhysicsEquation):
    """An extension of physics equation that allows for automatically changing the player's coordinates"""

    game_object = None
    current_time = 0
    is_started = False
    attribute_modifying = None
    height_of_path = 0
    time = 0
    max_time = 0
    last_time = 0
    has_max_time = False
    all_distance = 0
    last_delta_time = 0

    # def __init__(self, game_object=None, attribute_modifying="", height_of_path=0, initial_distance=0, time=.5):
    def __init__(self, **kwargs):
        """ Initializes the object

            :parameter game_object: GameObject; the game object that is following this path
            :parameter attribute_modifying: String; the name of the attribute this path is modifying
            :parameter time: float; the time to the vertex of the path
            :parameter height_of_path: float; the difference between the initial distance and the vertex of the path
            :parameter max_time: float; the max time of the path - the time the path should end

            :returns: None
        """

        self.game_object = get_kwarg_item(kwargs, "game_object", None)
        self.attribute_modifying = get_kwarg_item(kwargs, "attribute_modifying", "")
        self.time, self.height_of_path = get_kwarg_item(kwargs, "time", .5), get_kwarg_item(kwargs, "height_of_path", 0)
        self.initial_distance, self.max_time = get_kwarg_item(kwargs, "initial_distance", 0), get_kwarg_item(kwargs,
                                                                                                             "max_time",
                                                                                                             0)
        self.has_max_time = kwargs.get("max_time") is not None

        # Adding the initial_distance, so it that is the height of the parabola
        self.set_all_variables(self.height_of_path + self.initial_distance, self.time, self.initial_distance)

    def run(self, is_reset_event, is_start_event, is_using_everything=False, is_changing_coordinates=True):
        """ Runs the code for the game_object following the physics path

            :parameter is_reset_event: bool; if True it will call reset()
            :parameter is_start_event: bool; if True it will call start()
            :parameter is_using_everything: bool; if True it will use both velocity and acceleration and if False will just use velocity

            :returns: None
        """

        self.last_time = self.current_time

        # It should not be started again if it has already been started because starting puts the current_time back to 0
        if is_start_event and not self.is_started:
            self.start()

        if is_reset_event:
            self.reset()

        if self.is_started:
            self.current_time += VelocityCalculator.time

        can_change_coordinates = self.is_started and self.game_object is not None

        should_change_player_coordinates = can_change_coordinates and is_changing_coordinates

        self.last_delta_time = self.current_time - self.last_time

        # Decides if it is just using the velocity or both velocity and acceleration
        if should_change_player_coordinates and not is_using_everything:
            self.game_object.__dict__[self.attribute_modifying] += self.get_velocity_displacement()

        elif should_change_player_coordinates:
            self.game_object.__dict__[self.attribute_modifying] = self.get_distance(self.current_time)

    def start(self):
        """Starts the physics path"""

        self.is_started = True
        self.current_time = 0

    def reset(self):
        """Ends and reset the physics path"""

        self.is_started = False
        self.current_time = 0
        self.last_time = 0

    def set_initial_distance(self, initial_distance):
        """Sets the initial distance, so the height of the parabola is equal to the vertex"""

        self.initial_distance = initial_distance
        self.set_all_variables(self.initial_distance + self.height_of_path, self.time, self.initial_distance)

    def get_velocity_displacement(self):
        """:returns: float; the displacement from velocity (the last_time - start_time)"""

        current_distance = self.initial_velocity * self.current_time
        last_distance = self.initial_velocity * self.last_time

        return current_distance - last_distance

    def get_acceleration_displacement(self):
        """:returns: float; the distance from acceleration with gravity"""

        current_distance = 1 / 2 * self.acceleration * pow(self.current_time, 2)
        last_distance = 1 / 2 * self.acceleration * pow(self.last_time, 2)

        return current_distance - last_distance

    def get_total_displacement(self):
        """:returns: float; the displacement from both velocity and acceleration"""

        return self.get_velocity_displacement() + self.get_acceleration_displacement()

    def get_acceleration_displacement_from_time(self, time):
        """:returns: float; the displacement from acceleration at that time"""

        return 1 / 2 * self.acceleration * pow(time, 2)

    def get_final_velocity(self):
        """:returns: float; the velocity from acceleration (assumes initial_velocity is 0)"""

        return self.acceleration * self.current_time

    def is_done(self, should_reset=False):
        """:returns: bool; if the path is finished (and if 'should_reset' it will reset it)"""

        return_value = self.current_time >= self.max_time and self.has_max_time

        if should_reset and return_value:
            self.reset()

        return return_value

    def has_finished(self):
        """:returns: bool; if the path has either not started or is done"""

        return not self.is_started or self.is_done()
