import board
import digitalio
import time

class ButtonController:
    """
    Class to manage the hardware of physical buttons.
    Provides methods to check the state of each button.
    """
    def __init__(self):
        """
        Initializes the button controller by setting up the GPIO pins for the buttons.
        """
        try:
            # Inicializa cada boton como entrada con resistencia pull-up
            self.button_up = digitalio.DigitalInOut(board.D5)
            self.button_down = digitalio.DigitalInOut(board.D6)
            self.button_select = digitalio.DigitalInOut(board.D13)
            for btn in [self.button_up, self.button_down, self.button_select]:
                btn.direction = digitalio.Direction.INPUT
                btn.pull = digitalio.Pull.UP
        except Exception as e:
            # Si ocurre un error durante la inicialización, lo imprime y relanza la excepción
            print(f"[ButtonController] Error al inicializar los botones: {e}")
            raise

    def is_pressed(self, button):
        """
        Verifica si un botón está presionado.
        
        Args:
            button: Objeto DigitalInOut correspondiente al botón.
        
        Returns:
            bool: True si el botón está presionado, False en caso contrario.
        """
        try:
            # El valor es False cuando el boton esta presionado debido a la resistencia pull-up
            return not button.value
        except Exception as e:
            print(f"[ButtonController] Error al leer el estado del botón: {e}")
            return False

    def is_up_pressed(self):
        """
        Verifica si el botón 'arriba' está presionado.
        
        Returns:
            bool: True si el botón 'arriba' está presionado, False en caso contrario.
        """
        return self.is_pressed(self.button_up)

    def is_down_pressed(self):
        """
        Verifica si el botón 'abajo' está presionado.
        
        Returns:
            bool: True si el botón 'abajo' está presionado, False en caso contrario.
        """
        return self.is_pressed(self.button_down)

    def is_select_pressed(self):
        """
        Verifica si el botón 'seleccionar' está presionado.
        
        Returns:
            bool: True si el botón 'seleccionar' está presionado, False en caso contrario.
        """
        return self.is_pressed(self.button_select)
    
    def handle_navigation(self, total_items, current_index, draw_function):
        """
        Gestiona la navegación de un menú usando los botones 'arriba' y 'abajo'.
        Llama a la función de dibujo con el nuevo índice cuando se detecta un cambio.
        
        Args:
            total_items (int): Número total de elementos en el menú.
            current_index (int): Índice actual seleccionado.
            draw_function (callable): Función que redibuja el menú con el nuevo índice.
        
        Returns:
            int: El nuevo índice seleccionado después de la navegación.
        """
        if self.is_up_pressed():
            current_index = (current_index - 1) % total_items
            draw_function(current_index)
            time.sleep(0.2)# Evita rebotes y múltiples lecturas rápidas
        elif self.is_down_pressed():
            current_index = (current_index + 1) % total_items
            draw_function(current_index)
            time.sleep(0.2)
        return current_index