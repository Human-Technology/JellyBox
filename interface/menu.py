class Menu:
    """
    Class that defines the menus and their options for the user interface.
    """

    def __init__(self):
        # Main menu
        self.select_menu = ""
        self.main_menu_items = [
            "Mount/Unmount USB",
            "Web Templates",
            "Network Information",
            "Restart Server",
            "Shutdown Server"
        ]
        # Web templates submenu
        self.web_menu_items = [
            "Terminal",
            "CyberPunk",
            "Back"
        ]

    def get_len_main_menu_items(self) -> int:
        """
        Returns the number of options in the main menu.
        """
        return len(self.main_menu_items)
    
    def get_len_web_menu_items(self) -> int:
        """
        Returns the number of options in the web submenu.
        """
        return len(self.web_menu_items)