import os
from tkinter import Tk, Label, Button, filedialog, Menu
from PIL import ImageTk, Image
import geoAnnotatorLabeler as gal

class ImageBrowser:
    def __init__(self):
        self.folder_path = ""
        self.images = []
        self.current_index = 0

        self.window = Tk()
        self.window.title("GeoAnnotator")
        self.window.geometry("800x500")

        self.image_label = Label(self.window)
        self.image_label.pack(pady=10)

        self.previous_button = Button(self.window, text="Previous", command=self.show_previous)
        self.previous_button.pack(side="left", padx=10)

        self.next_button = Button(self.window, text="Next", command=self.show_next)
        self.next_button.pack(side="right", padx=10)

        self.choose_button = Button(self.window, text="Choose", command=self.choose_image)
        self.choose_button.pack(pady=10)

        self.create_menu()

        self.show_current_image()

    def create_menu(self):
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
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
        if self.images:
            image_path = self.images[self.current_index]
            image = Image.open(image_path)
            
            # Keep the aspect ratio of the images
            width, height = image.size
            #image = image.resize((400, 400), Image.LANCZOS)
            image = image.resize((width//2, height//2), Image.LANCZOS)

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

if __name__ == "__main__":
    image_browser = ImageBrowser()
    image_browser.window.mainloop()
