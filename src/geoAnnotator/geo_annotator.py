import os
import cv2
import numpy as np
from tkinter import *
from tkinter import Label, Tk, Button, ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
from PIL import ImageTk, Image

# Main window
window = Tk()
window.geometry("1200x720")
window.title("App")
#window.iconbitmap("path/here/icon.ico")

# Create menu
main_menu = Menu(window)
window.config(menu=main_menu)

print(os.path.expanduser('~\Documents'))



def new_project_window():
    top_window = Toplevel(window)
    top_window.geometry("640x640")
    top_window.title("New Project")
    #window.iconbitmap("path/here/icon.ico")
    top_window.grab_set()

    test_label_A = Label(top_window, text="test A", font=("Heveltica, 14"))
    test_label_A.pack(pady=5, padx=5)
    test_label_B = Label(top_window, text="test B", font=("Heveltica, 14"))
    test_label_B.pack(pady=5, padx=5)

    # Create new project menu
    new_project_window_menu = Menu(top_window)
    top_window.config(menu=new_project_window_menu)

    def exit_new_project():
        top_window.destroy()
        top_window.update()

    ##############test############

    # Open image
    def open_image():

        global panel_image
        # Open a file chooser dialog and allow the user to select an input
        # Image
        img_path = filedialog.askopenfilename()
        # ensure a file path was selected
        if len(img_path) > 0:
            # load the image from disk
            image_to_open = cv2.imread(img_path)
            # convert the images to PIL format...
            image_to_open = Image.fromarray(image_to_open)
            # ...and then to ImageTk format
            image_to_open = ImageTk.PhotoImage(image_to_open)

            # if the panels are None, initialize them
            if panel_image is None:
                # The panel image will store our original image
                panel_image = Label(top_window, image=image_to_open)
                panel_image.image_to_open = image_to_open
                panel_image.pack(side="left", padx=5, pady=5)
                #pass

            else:
                # update the panel
                panel_image.configure(image=image_to_open)
                panel_image.image_to_open = image_to_open

# initialize the image panels
#panel_image = None

    

    ##############test############

    # Add new project file menu
    new_project_menu = Menu(new_project_window_menu, tearoff=False)
    new_project_window_menu.add_cascade(label="Project file", menu=new_project_menu)
    new_project_menu.add_command(label="Save this project", command=save_project)
    new_project_menu.add_command(label="Open image in project", command=open_image)
    new_project_menu.add_command(label="Exit", command=exit_new_project)
    

# TEMP: Just a test button
#test_button = Button(window, text="Open window", command=new_project_window)
#test_button.pack(pady=50, padx=50)

panel_image = None

def create_new_project():
    new_project_window()

def open_project():
    pass

def save_project():
    pass

def exit_application():
    window.quit()



# Add main file menu
file_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Project", command=create_new_project)
file_menu.add_command(label="Open Project", command=open_project)
#file_menu.add_command(label="Save", command=save_project)
file_menu.add_command(label="Exit", command=exit_application)

mainloop()