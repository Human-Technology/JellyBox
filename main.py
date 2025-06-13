import logging
import os
import time
from interface.interface import Interface
from input.button_action import ButtonAction
from input.button_controller import ButtonController

# Determines the path of the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "jellybox.log")

# Logging configuration
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def handle_menu(menu_name, get_len_func, draw_func, execute_func, interface, buttons, selected_index):
    """
    Handles menu navigation and selection.
    """
    selected_index = buttons.handle_navigation(get_len_func(), selected_index, draw_func)
    if buttons.is_select_pressed():
        try:
            execute_func(selected_index)
        except Exception as e:
            logging.error(f"Error executing action in menu '{menu_name}': {e}")
        # Reset the index if the menu is changed
        if interface.menu.select_menu != menu_name:
            selected_index = 0
        time.sleep(0.2)
    return selected_index

def main():
    interface = Interface()
    action = ButtonAction(interface)
    buttons = ButtonController()

    selected_index = 0
    interface.draw_main_menu(selected_index)

    logging.info("JellyBox started successfully.")

    while True:
        try:
            menu_name = interface.menu.select_menu

            if menu_name == "main":
                selected_index = handle_menu(
                    "main",
                    interface.menu.get_len_main_menu_items,
                    interface.draw_main_menu,
                    action.execute_action_main,
                    interface, buttons, selected_index
                )
            elif menu_name == "web":
                selected_index = handle_menu(
                    "web",
                    interface.menu.get_len_web_menu_items,
                    interface.draw_web_menu,
                    action.execute_action_web,
                    interface, buttons, selected_index
                )
            elif menu_name == "device":
                selected_index = handle_menu(
                    "device",
                    lambda: interface.command.get_devices_len() + 1,
                    interface.draw_device_menu,
                    action.execute_action_device,
                    interface, buttons, selected_index
                )
            elif menu_name == "red":
                if buttons.is_select_pressed():
                    try:
                        action.execute_action_back()
                    except Exception as e:
                        logging.error(f"Error executing action in 'network' menu: {e}")
                    selected_index = 0
                    time.sleep(0.2)
        except KeyboardInterrupt:
            logging.info("JellyBox detenido por el usuario.")
            break
        except Exception as e:
            logging.critical(f"Unexpected error in the main loop: {e}", exc_info=True)
            time.sleep(1)  # Prevents fast loops in case of error

if __name__ == '__main__':
    main()