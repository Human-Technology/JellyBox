from interface.command import Command

class ButtonAction:
    """
    Class responsible for handling button actions in the user interface.
    This class defines methods to execute specific actions based on the index of the pressed button.
    """

    def __init__(self, interface, command=None):
        """
        Initializes the class with the user interface and the Command object.
        
        :param interface: Instance of the user interface that handles display and navigation.
        :type interface: Interface
        :param command: Instance of the Command class that handles system actions (optional).
        :type command: Command
        """
        self.interface = interface
        self.command = command or Command()

        # Dictionary that maps indices to action functions for the main menu
        self.main_actions = {
            0: lambda: self.interface.draw_device_menu(0),
            1: lambda: self.interface.draw_web_menu(0),
            2: lambda: self.interface.draw_network_information(),
            3: self.command.reboot_system,
            4: self.command.shut_down_system,
        }

        # Dictionary for web menu actions
        self.web_actions = {
            0: lambda: self._web_action_update_and_draw("index_retro", 0),
            1: lambda: self._web_action_update_and_draw("index_cyberpunk", 1),
            2: lambda: self.interface.draw_main_menu(0),
        }

        # Dictionary for device menu actions
        self.device_actions = {
            0: lambda: self.interface.show_device_status(),
            1: lambda: self.interface.restart_device(),
        }

    def execute_action_main(self, index):
        """
        Executes the action corresponding to the received index in the main menu.
        Args:
            index (int): Index of the action to execute.
        """
        try:
            action = self.main_actions.get(index)
            if action:
                action()
            else:
                print(f"[ButtonAction] Action not defined for index: {index} (main)")
        except Exception as e:
            print(f"[ButtonAction] Error executing action {index} (main): {e}")

    def execute_action_web(self, index):
        """
        Executes the action corresponding to the received index in the web menu.
        Args:
            index (int): Index of the action to execute.
        """
        try:
            action = self.web_actions.get(index)
            if action:
                action()
            else:
                print(f"[ButtonAction] Action not defined for index: {index} (web)")
        except Exception as e:
            print(f"[ButtonAction] Error executing action {index} (web): {e}")


    def execute_action_device(self, index):
        """
        Executes the action corresponding to the received index in the device menu.
        If the index is equal to the number of devices, it returns to the main menu.
        Otherwise, it executes the custom device action and returns to the main menu.
        Args:
            index (int): Index of the action to execute.
        """
        if self.command.get_devices_len() == index:
            self.interface.draw_main_menu(0)
        else:
            self.command.custom_device(index)
            self.interface.draw_main_menu(0)
    
    def execute_action_back(self):
        self.interface.draw_main_menu(0)

    def _web_action_update_and_draw(self, website, index):
        """
        Updates the website and draws the selection on the interface.
        Args:
            website (str): Name of the website.
            index (int): Selected index.
        """
        try:
            self.command.update_website(website)
            self.interface.draw_web_selected(index)
        except Exception as e:
            print(f"[ButtonAction] Error en _web_action_update_and_draw: {e}")       
        