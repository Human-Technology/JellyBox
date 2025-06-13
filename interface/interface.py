import logging
import time
from PIL import Image, ImageDraw, ImageFont
from .display import Display
from .menu import Menu
from .command import Command

class Interface:
    """
    Main class to manage the system's graphical interface.
    Encapsulates the logic for drawing menus, headers, and information screens.
    """

    # Definition of colors and font as class constants
    COLOR_GREEN = (0, 255, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_SELECTED_BG = (50, 50, 50)
    FONT = ImageFont.load_default()

    def __init__(self):
        """
        Initializes the interface components: display, menus, and commands.
        """
        self.display = Display()
        self.menu = Menu()
        self.command = Command()
        self.disp = self.display.disp
        self.image = self.display.image
        self.draw = self.display.draw

    def _clear_screen(self):
        """
        Clears the screen with the background color.
        """
        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), fill=self.COLOR_BLACK)

    def _draw_frame(self):
        """
        Draws a frame around the screen.
        """
        self.draw.rectangle((2, 2, self.disp.width - 2, self.disp.height - 2), outline=self.COLOR_GREEN)

    def _draw_header(self):
        """
        Draws the header with the title and server IP.
        """
        try:
            self.draw.text((50, 10), "JellyBox", fill=self.COLOR_WHITE, font=self.FONT)
            ip = self.command.get_ip_access_point()
            self.draw.text((40, 20), f"Server IP: {ip}", fill=self.COLOR_WHITE, font=self.FONT)
        except Exception as e:
            logging.error(f"Error drawing header: {e}", exc_info=True)

    def draw_main_menu(self, selected_index):
        """
        Draws the main menu, highlighting the selected option.
        Args:
            selected_index (int): Index of the selected option.
        """
        self.menu.select_menu = "main"
        self._clear_screen()
        self._draw_frame()
        self._draw_header()

        for idx, label in enumerate(self.menu.main_menu_items):
            y = 50 + idx * 30
            is_selected = (idx == selected_index)
            bg_color = self.COLOR_SELECTED_BG if is_selected else self.COLOR_BLACK
            text_color = self.COLOR_GREEN if is_selected else self.COLOR_WHITE

            self.draw.rectangle((10, y, self.disp.width - 10, y + 25), fill=bg_color)
            self.draw.text((15, y + 3), label, fill=text_color, font=self.FONT)

        self.disp.image(self.image)

    def draw_web_menu(self, selected_index):
        """
        Draws the web templates submenu, highlighting the selected option.
        Args:
            selected_index (int): Index of the selected option.
        """
        self.menu.select_menu = "web"
        self._clear_screen()
        self._draw_frame()
        self._draw_header()

        for idx, label in enumerate(self.menu.web_menu_items):
            y = 50 + idx * 30
            is_selected = (idx == selected_index)
            bg_color = self.COLOR_SELECTED_BG if is_selected else self.COLOR_BLACK
            text_color = self.COLOR_GREEN if is_selected else self.COLOR_WHITE

            self.draw.rectangle((10, y, self.disp.width - 10, y + 25), fill=bg_color)
            self.draw.text((15, y + 3), label, fill=text_color, font=self.FONT)

        self.disp.image(self.image)

    def draw_device_menu(self, selected_index):
        """
        Draws the menu of connected USB devices and the 'back' option.
        Args:
            selected_index (int): Index of the selected option.
        """
        self.menu.select_menu = "device"
        self._clear_screen()
        self._draw_frame()
        self._draw_header()

        try:
            devices = self.command.get_device_usb()
            options = [
                f"USB-{d['NAME']} {d['SIZE']}" + (" Mounted" if d['MOUNTPOINT'] else "")
                for d in devices
            ]
            options.append("Back")

            for idx, label in enumerate(options):
                y = 50 + idx * 30
                is_selected = (idx == selected_index)
                bg_color = self.COLOR_SELECTED_BG if is_selected else self.COLOR_BLACK
                text_color = self.COLOR_GREEN if is_selected else self.COLOR_WHITE

                self.draw.rectangle((10, y, self.disp.width - 10, y + 25), fill=bg_color)
                self.draw.text((15, y + 3), label, fill=text_color, font=self.FONT)

            self.disp.image(self.image)
        except Exception as e:
            logging.error(f"Error dibujando menú de dispositivos: {e}", exc_info=True)

    def draw_web_selected(self, index):
        """
        Shows a confirmation screen when selecting a web template.
        Args:
            index (int): Index of the selected template.
        """
        self._clear_screen()
        self._draw_frame()
        self.draw.text((40, 20), "Web Selected", fill=self.COLOR_WHITE, font=self.FONT)
        self.disp.image(self.image)
        time.sleep(2)
        self.draw_web_menu(index)

    def draw_network_information(self):
        """
        Shows network information and the Wi-Fi access QR code.
        """
        self.menu.select_menu = "red"
        self._clear_screen()
        self._draw_frame()
        try:
            ssid = self.command.get_SSID()
            pwd = self.command.get_password_access_point()

            self.draw.text((40, 20), "Access Point Information", fill=self.COLOR_WHITE, font=self.FONT)
            self.draw.text((10, 40), f"SSID: {ssid}", fill=self.COLOR_WHITE, font=self.FONT)
            self.draw.text((10, 60), f"Password: {pwd}", fill=self.COLOR_WHITE, font=self.FONT)

            # Generate and show QR
            self.command.get_qr_access_point()
            qr = Image.open("wifi_qr.png").resize((150, 150))
            self.image.paste(qr, (10, 80))

            # Back button
            self.draw.rectangle((10, 250, self.disp.width - 10, 280), fill=self.COLOR_SELECTED_BG)
            self.draw.text((10, 255), "Back", fill=self.COLOR_WHITE, font=self.FONT)

            self.disp.image(self.image)
        except Exception as e:
            logging.error(f"Error showing network information: {e}", exc_info=True)