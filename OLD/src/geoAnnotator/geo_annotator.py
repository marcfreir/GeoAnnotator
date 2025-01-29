import os
from tkinter import Tk, Label, Button, filedialog, Menu, Frame, ttk
from PIL import ImageTk, Image
import geoAnnotatorLabeler as gal

class ImageBrowser:
    def __init__(self):
        self.folder_path = ""
        self.images = []
        self.current_index = 0

        self.window = Tk()
        self.window.title("GeoAnnotator")
        self.window.geometry("1200x720")

        self.image_label = Label(self.window)
        self.image_label.pack(pady=10)

        self.separator = ttk.Separator(self.window, orient="horizontal")
        self.separator.pack(fill="x", padx=10, pady=5)

        self.choose_button = Button(self.window, text="Choose", command=self.choose_image)
        self.choose_button.pack(pady=5)

        self.status_label = Label(self.window, text="", bd=1, relief="sunken", anchor="w")
        self.status_label.pack(fill="x")

        self.button_frame = Frame(self.window)
        self.button_frame.pack(pady=10)

        self.previous_button = Button(self.button_frame, text="Previous", command=self.show_previous)
        self.previous_button.pack(side="left", padx=10)

        self.next_button = Button(self.button_frame, text="Next", command=self.show_next)
        self.next_button.pack(side="right", padx=10)

        self.create_menu()

        self.show_current_image()

    def create_menu(self):
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Create Project Path", command=self.create_project_path)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

    def open_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.images = self.load_images()
            self.current_index = 0
            self.show_current_image()

    def load_images(self):
        image_extensions = [".jpg", ".jpeg", ".png", ".gif"]  # Add more extensions if needed
        images = []
        for file_name in os.listdir(self.folder_path):
            if os.path.splitext(file_name)[1].lower() in image_extensions:
                images.append(os.path.join(self.folder_path, file_name))
        return images
    
    def show_current_image(self):
        default_image_path = "./GeoAnnotator/src/geoAnnotator/assets/geoAnnotator_main_frame.png"

        if self.images:
            image_path = self.images[self.current_index]
            image = Image.open(image_path)
        else:
            try:
                image = Image.open(default_image_path)
            except FileNotFoundError:
                # Create a blank image if the default image is not found
                image = Image.new("RGB", (1, 1), "white")

        # Resize the image to have a fixed height of 540 pixels while preserving the aspect ratio
        height = 540
        width = int((height / image.size[1]) * image.size[0])
        image = image.resize((width, height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo





    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_image()

    def show_next(self):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.show_current_image()

    def choose_image(self):
        if self.images:
            image_path = self.images[self.current_index]
            gal.draw_polygon(image_path)

    def create_project_path(self):
        project_path = filedialog.askdirectory()
        if project_path:
            if not os.path.exists(project_path):
                os.makedirs(project_path)
                self.status_label.configure(text="New project created on: " + project_path)
            else:
                self.status_label.configure(text="Path already exists.")


if __name__ == "__main__":
    image_browser = ImageBrowser()
    image_browser.window.mainloop()
