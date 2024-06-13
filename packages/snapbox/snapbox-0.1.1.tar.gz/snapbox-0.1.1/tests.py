import tkinter as tk
import unittest
from tkinter import ttk
from unittest.mock import MagicMock

from PIL import Image
from snapbox import SnapBoxApp

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("TestSnapBoxApp",)


class TestSnapBoxApp(unittest.TestCase):

    def setUp(self) -> None:
        # Set up the test environment
        self.root = tk.Tk()
        self.app = SnapBoxApp(self.root)

    def tearDown(self) -> None:
        # Tear down the test environment
        self.root.destroy()

    def test_initialization(self) -> None:
        # Test if the main components are initialized correctly
        self.assertIsInstance(self.app.path_entry, ttk.Entry)
        self.assertIsInstance(self.app.browse_button, ttk.Button)
        self.assertIsInstance(self.app.canvas, tk.Canvas)
        self.assertIsInstance(self.app.format_menu, ttk.Combobox)
        self.assertIsInstance(self.app.coord_frame, ttk.LabelFrame)
        self.assertIsInstance(self.app.line_frame, ttk.LabelFrame)

    def test_load_image(self) -> None:
        # Create a real image for testing
        test_image = Image.new("RGB", (100, 100), color="red")
        self.app.original_img = test_image
        self.app.show_image(test_image)
        self.assertEqual(self.app.original_img.size, (100, 100))

    def test_add_update_rectangle(self) -> None:
        # Test the add_update_rectangle function
        self.app.coord_entries[0].insert(0, "10")
        self.app.coord_entries[1].insert(0, "20")
        self.app.coord_entries[2].insert(0, "30")
        self.app.coord_entries[3].insert(0, "40")
        self.app.thickness_entry.delete(0, tk.END)  # Clear any existing value
        self.app.thickness_entry.insert(0, "2")
        self.app.line_color = "#ff0000"
        self.app.add_update_rectangle()
        self.assertEqual(len(self.app.rectangles), 1)
        self.assertEqual(
            self.app.rectangles[0],
            ([10, 20, 30, 40], "x, y, width, height", 2, "#ff0000"),
        )

    def test_zoom_in(self) -> None:
        # Test the zoom_in function
        initial_zoom = self.app.zoom_factor
        self.app.zoom_in()
        self.assertGreater(self.app.zoom_factor, initial_zoom)

    def test_zoom_out(self) -> None:
        # Test the zoom_out function
        initial_zoom = self.app.zoom_factor
        self.app.zoom_out()
        self.assertLess(self.app.zoom_factor, initial_zoom)

    def test_drag_image(self) -> None:
        # Create a real image for testing
        test_image = Image.new("RGB", (100, 100), color="red")
        self.app.show_image(test_image)

        # Simulate pressing the mouse button at coordinates (100, 100)
        self.app.on_button_press(MagicMock(x=100, y=100))

        # Simulate dragging the mouse to coordinates (110, 110)
        self.app.on_mouse_drag(MagicMock(x=110, y=110))

        # Simulate releasing the mouse button
        self.app.on_button_release(MagicMock())

        # Check if drag data has been reset
        self.assertEqual(self.app.drag_data["x"], 0)
        self.assertEqual(self.app.drag_data["y"], 0)


if __name__ == "__main__":
    unittest.main()
