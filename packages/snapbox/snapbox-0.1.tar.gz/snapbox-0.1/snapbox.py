import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageDraw, ImageTk


class RectangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("snapbox: Draw boxes over image")

        # Style Configuration
        style = ttk.Style()
        style.theme_use("clam")  # The clam (modern) theme
        style.configure(
            "TButton",
            background="#333",
            foreground="white",
            font=("Helvetica", 10),
        )
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("TEntry", font=("Helvetica", 10))
        style.configure("TCombobox", font=("Helvetica", 10))
        style.configure("TLabelframe", background="#f0f0f0")
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

        # Dropdown for selecting rectangle format
        self.format_var = tk.StringVar()
        self.format_choices = {
            "x, y, width, height",
            "min_x, min_y, max_x, max_y",
        }
        self.format_var.set("x, y, width, height")  # default input format
        self.format_var.trace("w", self.update_labels)

        self.format_menu = ttk.Combobox(
            root,
            textvariable=self.format_var,
            values=list(self.format_choices),
            state="readonly",
        )
        self.format_menu.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Rectangle specification frame
        self.rect_frame = ttk.LabelFrame(root, text="Add/Edit Rectangle")
        self.rect_frame.grid(
            row=3, column=0, columnspan=3, sticky="ew", padx=10
        )

        self.labels = ["X:", "Y:", "Width:", "Height:"]
        self.label_widgets = [
            ttk.Label(self.rect_frame, text=label) for label in self.labels
        ]
        self.coord_entries = [
            ttk.Entry(self.rect_frame, width=10) for _ in range(4)
        ]

        for i, (label, entry) in enumerate(
            zip(self.label_widgets, self.coord_entries)
        ):
            label.grid(row=0, column=2 * i)
            entry.grid(row=0, column=2 * i + 1)

        self.add_button = ttk.Button(
            self.rect_frame,
            text="Add/Update Rectangle",
            command=self.add_update_rectangle,
        )
        self.add_button.grid(row=0, column=8)

        # Button to generate rectangles on the image
        self.generate_button = ttk.Button(
            root, text="Generate on Image", command=self.generate_rectangles
        )
        self.generate_button.grid(
            row=4, column=0, columnspan=3, sticky="ew", pady=10
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
        self.listbox.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)

        self.delete_button = ttk.Button(
            root, text="Delete Selected", command=self.delete_rectangle
        )
        self.delete_button.grid(row=5, column=2, sticky="ew")

        self.rectangles = []
        self.img = None
        self.original_img = None
        self.tkimg = None

    def update_labels(self, *args):
        format_choice = self.format_var.get()
        new_labels = ["X:", "Y:", "Width:", "Height:"]
        if format_choice == "x, y, width, height":
            new_labels = ["X:", "Y:", "Width:", "Height:"]
        elif format_choice == "min_x, min_y, max_x, max_y":
            new_labels = ["Min X:", "Min Y:", "Max X:", "Max Y:"]

        for label_widget, new_label in zip(self.label_widgets, new_labels):
            label_widget.configure(text=new_label)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)
            self.original_img = Image.open(file_path)
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
                new_height = canvas_height
                new_width = int(new_height * image_aspect_ratio)
            else:
                new_width = canvas_width
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
            )

    def resize_image(self, event=None):
        if self.tkimg:  # Only update if an image is loaded
            self.update_image_display()

    def add_update_rectangle(self):
        format_var = self.format_var.get()
        try:
            coords = [int(entry.get()) for entry in self.coord_entries]
            rectangle = (coords, format_var)
            self.listbox.insert(tk.END, f"{format_var}: {coords}")
            self.rectangles.append(rectangle)
            self.clear_entries()
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter valid integers for rectangle dimensions."
            )

    def delete_rectangle(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            del self.rectangles[index]
        except Exception:
            messagebox.showerror("Error", "Select a rectangle to delete.")

    def clear_entries(self):
        for entry in self.coord_entries:
            entry.delete(0, tk.END)

    def generate_rectangles(self):
        if self.original_img:
            temp_img = self.original_img.copy()
            draw = ImageDraw.Draw(temp_img)
            for coords, format_var in self.rectangles:
                if format_var == "x, y, width, height":
                    x, y, width, height = coords
                    draw.rectangle(
                        [x, y, x + width, y + height], outline="red", width=2
                    )
                elif format_var == "min_x, min_y, max_x, max_y":
                    min_x, min_y, max_x, max_y = coords
                    draw.rectangle(
                        [min_x, min_y, max_x, max_y], outline="red", width=2
                    )
            self.show_image(temp_img)


def main():
    root = tk.Tk()
    root.geometry("800x600")  # Initial size of the window
    app = RectangleApp(root)  # noqa
    root.mainloop()


if __name__ == "__main__":
    main()
