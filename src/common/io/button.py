from gpiozero import Button
import time


class SnoozeButton:
    """Handles snooze button input with debouncing"""
    
    def __init__(self, button_pin=27, hold_time=0.1):
        """
        Initialize the snooze button.
        
        Args:
            button_pin: GPIO pin number for the button
            hold_time: Time to hold button before registering (debounce)
        """
        self.button = Button(button_pin, hold_time=hold_time)
        self.pressed = False
        self.button.when_pressed = self._on_press
        self.button.when_released = self._on_release
    
    def _on_press(self):
        """Called when button is pressed"""
        self.pressed = True
    
    def _on_release(self):
        """Called when button is released"""
        self.pressed = False
    
    def is_pressed(self) -> bool:
        """Check if button is currently pressed"""
        return self.pressed
    
    def wait_for_press(self, timeout=None) -> bool:
        """
        Block until button is pressed or timeout occurs.
        
        Args:
            timeout: Maximum time to wait in seconds, None for indefinite
        
        Returns:
            True if button was pressed, False if timeout occurred
        """
        try:
            self.button.wait_for_press(timeout=timeout)
            return True
        except AttributeError:
            # Fallback: manual polling
            start = time.time()
            while not self.pressed:
                if timeout and (time.time() - start) > timeout:
                    return False
                time.sleep(0.01)
            return True
    
    def close(self):
        """Clean up button resources"""
        self.button.close()
