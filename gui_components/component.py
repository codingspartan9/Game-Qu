from game_qu.base.history_keeper import HistoryKeeper
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.dimensions import Dimensions
from game_qu.base.utility_functions import load_image, render_image, render_rectangle, mouse_is_clicked, is_mouse_collision
from game_qu.base.id_creator import id_creator


class Component(Dimensions):
    """ The components that are added to the game's window. If a screen's get_components() method returns a component,
        that components run and render methods will be called"""

    color = None
    path_to_image = None
    name = ""
    is_addable = True
    is_runnable = True  # Sometimes the screen has to run the player, so some components shouldn't be run
    last_frame_id_when_visible = 0

    def __init__(self, path_to_image=""):
        """Initializes the object and loads an image if the path_to_image is not empty"""

        self.path_to_image = path_to_image

        if path_to_image != "":
            load_image(path_to_image)

        self.name = id_creator.get_unique_id()

    def run(self):
        """Runs everything the component needs every game cycle"""

        pass

    def render(self):
        """ Renders the component onto the screen- it will either render the image if 'self.path_to_image' is not empty
            otherwise it will render a rectangle with the color from 'self.color'"""

        if self.path_to_image != "":
            render_image(self.path_to_image, self.left_edge, self.top_edge, self.length, self.height)

        else:
            render_rectangle(self.left_edge, self.top_edge, self.length, self.height, self.color)

        self.last_frame_id_when_visible = HistoryKeeper.get_frame_id(VelocityCalculator.current_cycle_number)

    def got_clicked(self):
        """:returns: bool; the mouse is over the component and the mouse was clicked"""

        was_visible_last_cycle = self.last_frame_id_when_visible == HistoryKeeper.last_frame_id
        return mouse_is_clicked() and is_mouse_collision(self) and was_visible_last_cycle