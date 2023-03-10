from game_qu.library_abstraction import utility_functions


class Window:
    """Shows everything onto the users screen through adding components to it and displaying those added components"""

    screens = []

    def __init__(self, length, height, BACKGROUND_COLOR, title):
        """ Creates a window with the length, height, and title of the values given

            :parameter length: int; the length of the window
            :parameter height: int; the height of the window
            :parameter BACKGROUND_COLOR: tuple; the (Red, Green, Blue) values of the window's background
            :parameter title: String; the title displayed of the window

            :returns: None
        """

        utility_functions.set_up_window(length, height, BACKGROUND_COLOR, title)

    def add_screen(self, screen):
        """Adds the screen to 'self.screens' so the Window keeps track of it"""

        self.screens.append(screen)

    def display_screen(self, screen):
        """ Makes all the other screen's invisible by setting their 'is_visible' attribute to False and makes the 'screen'
            visible by setting it's 'is_visible' attribute set to True"""

        for other_screen in self.screens:
            other_screen.is_visible = False

        screen.is_visible = True

    def run(self, should_render):
        """ Calls the run() and render_background() method of all visible screens. It will also call the run() and render()
            methods for each of the Component(s) that the get_components() method returns for the visible screens"""

        for screen in self.screens:
            if not screen.is_visible:
                continue

            if screen.is_visible:
                screen.run()

            if screen.is_visible and should_render:
                screen.render_background()

            for component in screen.get_components():

                if component.is_runnable:
                    component.run()

                if should_render:
                    component.render()
