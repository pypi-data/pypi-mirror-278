import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk

from PIL import Image, ImageDraw, ImageTk

__title__ = "snapbox"
__version__ = "0.1.1"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("SnapBoxApp",)


class SnapBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SnapBox: Draw boxes over image")
        self.tkimg = None
        self.setup_menu()

        # Style Configuration
        style = ttk.Style()
        style.theme_use("clam")  # The clam (modern) theme
        style.configure(
            "TButton",
            background="#333",
            foreground="white",
            font=("Helvetica", 10),
        )
        style.configure(
            "TLabel",
            background="#f0f0f0",
            font=("Helvetica", 10),
        )
        style.configure("TEntry", font=("Helvetica", 10))
        style.configure("TCombobox", font=("Helvetica", 10))
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", background="#f0f0f0")
        style.map("TButton", background=[("active", "#555")])

        # Allow window to be resizable
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Image path entry and browse button
        self.path_entry = ttk.Entry(root, width=40)
        self.path_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.browse_button = ttk.Button(
            root, text="Browse", command=self.load_image
        )
        self.browse_button.grid(row=0, column=1, padx=10, pady=10)

        # Canvas for image display
        self.canvas = tk.Canvas(root, bg="grey")
        self.canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Setup resize behavior
        self.root.bind("<Configure>", self.resize_image)

        # Zoom controls
        self.zoom_frame = ttk.Frame(root)
        self.zoom_frame.grid(
            row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=10
        )
        # Configure columns for centering
        self.zoom_frame.columnconfigure(0, weight=1)
        self.zoom_frame.columnconfigure(3, weight=1)

        self.zoom_in_button = ttk.Button(
            self.zoom_frame,
            text="Zoom In",
            command=self.zoom_in,
            padding=(10, 5),
        )
        self.zoom_in_button.grid(row=2, column=1, sticky="ew", padx=5)

        self.zoom_out_button = ttk.Button(
            self.zoom_frame,
            text="Zoom Out",
            command=self.zoom_out,
            padding=(10, 5),
        )
        self.zoom_out_button.grid(row=2, column=2, sticky="ew", padx=5)

        # Rectangle specification frame
        self.rect_frame = ttk.LabelFrame(root, text="Add/Edit Rectangle")
        self.rect_frame.grid(
            row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=10
        )

        # Coordinates frame
        self.coord_frame = ttk.LabelFrame(self.rect_frame, text="Coordinates")
        self.coord_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Dropdown for selecting rectangle format
        self.format_var = tk.StringVar()
        self.format_choices = {
            "x, y, width, height",
            "x_min, y_min, x_max, y_max",
        }
        self.format_var.set("x, y, width, height")  # default input format
        self.format_var.trace("w", self.update_labels)

        self.format_menu = ttk.Combobox(
            self.coord_frame,
            textvariable=self.format_var,
            values=list(self.format_choices),
            state="readonly",
        )
        self.format_menu.grid(row=0, column=0, sticky="ew")

        self.labels = ["X:", "Y:", "Width:", "Height:"]
        self.label_widgets = [
            ttk.Label(self.coord_frame, text=label) for label in self.labels
        ]
        self.coord_entries = [
            ttk.Entry(self.coord_frame, width=10) for _ in range(4)
        ]

        for i, (label, entry) in enumerate(
            zip(self.label_widgets, self.coord_entries)
        ):
            label.grid(row=0, column=2 * i + 2)
            entry.grid(row=0, column=2 * i + 3)

        # Line properties frame
        self.line_frame = ttk.LabelFrame(self.rect_frame, text="Line")
        self.line_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Line thickness entry
        ttk.Label(self.line_frame, text="Thickness:").grid(
            row=0, column=0, sticky="w"
        )
        self.thickness_entry = ttk.Entry(self.line_frame, width=10)
        self.thickness_entry.grid(row=0, column=1, sticky="w")
        self.thickness_entry.insert(0, "2")  # Default value

        # Color picker button
        ttk.Label(self.line_frame, text="Color:").grid(
            row=0, column=2, sticky="w"
        )
        self.color_button = ttk.Button(
            self.line_frame, text="Choose Color", command=self.choose_color
        )
        self.color_button.grid(row=0, column=4, sticky="w")
        self.color_display = ttk.Label(
            self.line_frame,
            text="      ",
            background="#000000",
            padding=(2, 2, 2, 2),
        )
        self.color_display.grid(row=0, column=3, sticky="w", padx=5)

        # Add/Update Rectangle button
        self.add_button = ttk.Button(
            self.rect_frame,
            text="Add/Update Rectangle",
            command=self.add_update_rectangle,
        )
        self.add_button.grid(row=0, column=2, padx=10, sticky="w")

        # Button to generate rectangles on the image
        self.generate_button = ttk.Button(
            root, text="Generate on Image", command=self.generate_rectangles
        )
        self.generate_button.grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=10,
            padx=10,
        )

        # Listbox for rectangles
        self.listbox = tk.Listbox(
            root,
            height=6,
            width=50,
            bd=1,
            relief="solid",
            font=("Helvetica", 10),
        )
        self.listbox.grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=10, padx=10
        )

        self.delete_button = ttk.Button(
            root, text="Delete Selected", command=self.delete_rectangle
        )
        self.delete_button.grid(row=5, column=2, sticky="ew", padx=10)

        self.rectangles = []
        self.img = None
        self.original_img = None
        self.tkimg = None
        self.line_color = "#000000"  # Default color
        self.zoom_factor = 1.0

        # Drag functionality variables
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # Bind mouse events for dragging
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def update_labels(self, *args):
        format_choice = self.format_var.get()
        new_labels = ["X:", "Y:", "Width:", "Height:"]
        if format_choice == "x, y, width, height":
            new_labels = ["X:", "Y:", "Width:", "Height:"]
        elif format_choice == "x_min, y_min, x_max, y_max":
            new_labels = ["X Min:", "Y Min:", "X Max:", "Y Max:"]

        for label_widget, new_label in zip(self.label_widgets, new_labels):
            label_widget.configure(text=new_label)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.line_color = color_code
            self.color_display.configure(background=color_code)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)
            self.original_img = Image.open(file_path)
            self.zoom_factor = 1.0
            self.show_image(self.original_img)

    def show_image(self, img):
        self.img = img.copy()
        self.update_image_display()

    def update_image_display(self):
        if self.img:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_aspect_ratio = self.img.width / self.img.height
            canvas_aspect_ratio = canvas_width / canvas_height

            if canvas_aspect_ratio > image_aspect_ratio:
                new_height = int(canvas_height * self.zoom_factor)
                new_width = int(new_height * image_aspect_ratio)
            else:
                new_width = int(canvas_width * self.zoom_factor)
                new_height = int(new_width / image_aspect_ratio)

            self.tkimg = ImageTk.PhotoImage(
                self.img.resize(
                    (new_width, new_height), Image.Resampling.LANCZOS
                )
            )
            self.canvas.create_image(
                (canvas_width - new_width) // 2,
                (canvas_height - new_height) // 2,
                anchor="nw",
                image=self.tkimg,
                tags="image",
            )

    def resize_image(self, event=None):
        if self.tkimg:  # Only update if an image is loaded
            self.update_image_display()

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_image_display()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_image_display()

    def add_update_rectangle(self):
        format_var = self.format_var.get()
        try:
            coords = [int(entry.get()) for entry in self.coord_entries]
            thickness = int(self.thickness_entry.get())
            color = self.line_color
            rectangle = (coords, format_var, thickness, color)
            self.listbox.insert(
                tk.END,
                f"{format_var}: {coords}, {thickness}px, {color}",
            )
            self.rectangles.append(rectangle)
            self.clear_entries()
            self.color_display.configure(background=color)  # Retain color
        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter integers for box dimensions and thickness.",
            )

    def delete_rectangle(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            del self.rectangles[index]
        except Exception:
            messagebox.showerror(
                "Error",
                "Select a rectangle to delete.",
            )

    def clear_entries(self):
        for entry in self.coord_entries:
            entry.delete(0, tk.END)

    def generate_rectangles(self):
        if self.original_img:
            self.zoom_factor = 1.0
            temp_img = self.original_img.copy()
            draw = ImageDraw.Draw(temp_img)
            for coords, format_var, thickness, color in self.rectangles:
                if format_var == "x, y, width, height":
                    x, y, width, height = map(int, coords)
                    draw.rectangle(
                        [x, y, x + width, y + height],
                        outline=color,
                        width=thickness,
                    )
                elif format_var == "x_min, y_min, x_max, y_max":
                    x_min, y_min, x_max, y_max = map(int, coords)
                    draw.rectangle(
                        [x_min, y_min, x_max, y_max],
                        outline=color,
                        width=thickness,
                    )
            self.show_image(temp_img)

    def on_button_press(self, event):
        # Save the current mouse position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_mouse_drag(self, event):
        # Calculate the distance moved by the mouse
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        # Move the canvas
        self.canvas.move("image", dx, dy)

        # Update the drag data
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_button_release(self, event):
        # Reset the drag data
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def create_about_window(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About imgbox")
        about_window.geometry("400x300")

        tab_control = ttk.Notebook(about_window)

        # About Tab
        about_tab = ttk.Frame(tab_control)
        tab_control.add(about_tab, text="About")
        about_text = tk.Text(about_tab, height=10, width=50, wrap="word")
        about_text.insert(
            "end",
            (
                "SnapBox is a simple graphical tool for drawing rectangles "
                "on images."
            ),
        )
        about_text.config(state="disabled")
        about_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Author Tab
        author_tab = ttk.Frame(tab_control)
        tab_control.add(author_tab, text="Author")
        author_text = tk.Text(author_tab, height=10, width=50, wrap="word")
        author_text.insert(
            "end",
            (
                "Developed by Artur Barseghyan. For feedback and support, "
                "see https://github.com/barseghyanartur/snapbox#support."
            ),
        )
        author_text.config(state="disabled")
        author_text.pack(expand=True, fill="both", padx=10, pady=10)

        # License Tab
        license_tab = ttk.Frame(tab_control)
        tab_control.add(license_tab, text="License")
        license_text = tk.Text(license_tab, height=10, width=50, wrap="word")
        license_text.insert(
            "end",
            (
                "This software is released under the MIT License. "
                "See https://github.com/barseghyanartur/snapbox#license for"
                "more information."
            ),
        )
        license_text.config(state="disabled")
        license_text.pack(expand=True, fill="both", padx=10, pady=10)

        tab_control.pack(expand=True, fill="both")

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(
            label="About imgbox",
            command=self.create_about_window,
        )


def main():
    root = tk.Tk()
    root.geometry("800x600")  # Initial size of the window
    app = SnapBoxApp(root)  # noqa
    root.mainloop()


if __name__ == "__main__":
    main()
