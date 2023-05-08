import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
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

# Create main menu
main_menu = Menu(window)
window.config(menu=main_menu)

def exit_application():
    #window.quit()
    window.destroy()
    

##### Create OS path to save image #####
def create_project_path():
    # Create path on OS
    global path_to_save_image

    ######THIS IS TEMPORARY... NEED TO OPEN A SPECIFIC PATH AND SAVE INTO THE VARIABLE
    #path_to_save_image = "./test/LAB/RESULT_SCRATCH/"
    path_to_save_image = filedialog.askdirectory()
    print("SHAWASKA in 'create_project_path()'")
    print(path_to_save_image)

    # Check if path already exists
    if not os.path.exists(path_to_save_image):
    #if not os.chdir(path_to_save_image):
        os.mkdir(path_to_save_image)
        
        directory = ("Directory '% s' created" % path_to_save_image)
        print(directory)

        directory_path = os.path.abspath(path_to_save_image)
        directory_path_to_label = ("Project path created on: '%s'" % directory_path)
        directory_label = Label(window, text=directory_path_to_label)
        #directory_label.pack(side="left", padx=20, pady=400)
        directory_label.place(x=20, y=10)
    else:
        directory_path = os.path.abspath(path_to_save_image)
        directory_path_to_label = ("Project already created in path created on: '%s'" % directory_path)
        directory_label = Label(window, text=directory_path_to_label)
        #directory_label.pack(side="left", padx=20, pady=400)
        directory_label.place(x=20, y=10)


#############

# Global variables to draw polygon on selected image
#global done
done = False
global polygon_points
polygon_points = []
global current_polygon_point
current_polygon_point = (0,0)
global prev_current_point
prev_current_point = (0,0)
global image_number
image_number = 0

#############
# Draw with mouse
def on_mouse(event, x, y, buttons, user_param):
    global done, polygon_points, current_polygon_point, image_temp, image

    # Mouse callback that gets called for every mouse event (i.e. moving, clicking, etc.)
    if done: # Nothing more to do
        return
    if event == cv2.EVENT_MOUSEMOVE:
        # We want to be able to draw the line-in-progress, so update current mouse position
        current_polygon_point = (x, y)
    elif event == cv2.EVENT_LBUTTONDOWN:
        # Left click means adding a point at current position to the list of points
        print("Adding point #%d with position(%d,%d)" % (len(polygon_points), x, y))
        cv2.circle(image,(x,y),5,(0,200,0),-1)
        polygon_points.append((x, y))
        #print("Buguela: ", polygon_points)
        global set_of_points
        set_of_points = polygon_points
        global path_to_save_image
        try:
            set_of_points_file_path = (path_to_save_image+"/set_of_points.txt")
            set_of_points_file = open(set_of_points_file_path,"w")
            add_set_of_points = repr(set_of_points)
            set_of_points_file.write(add_set_of_points)
            set_of_points_file.close
        except NameError:
            print("Directory not created!")
            no_directory_created = "WARNING! The directory was not created before. The set of points was not created!"
            no_directory_created_error = Label(window, text=no_directory_created)
            no_directory_created_error.place(x=20, y=40)


        image_temp = image.copy()
    elif event == cv2.EVENT_RBUTTONDOWN:
        # Right click means we're done
        print("Completing polygon with %d points." % len(polygon_points))
        done = True

#############

opened_image = False

def open_image_to_mask():
    global image_path
    image_path = filedialog.askopenfilename()


    if image_path is None:
        return 0
    else:
        global image
        image = cv2.imread(image_path)

        if image is None:
            return
        else:
            global image_clone
            image_clone = image.copy()
            global image_temp
            image_temp = image.copy()



    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_mouse)

    global done
    while(not done):
        # This is our drawing loop, we just continuously draw new images
        # and show them in the named window
        if (len(polygon_points) > 1):
            if(current_polygon_point != prev_current_point):
                image = image_temp.copy()
            # Draw all the current polygon segments
            cv2.polylines(image, [np.array(polygon_points)], False, (255,0,0), 1)
            # And  also show what the current segment would look like
            cv2.line(image, (polygon_points[-1][0],polygon_points[-1][1]), current_polygon_point, (0,255,0))

        # Update the window
        cv2.imshow("image", image)
        # And wait 50ms before next iteration (this will pump window messages meanwhile)

        if cv2.waitKey(50) == ord('d'): # press d(done)
            done = True

    # User finised entering the polygon points, so let's make the final drawing
    image = image_clone.copy()
    # of a filled polygon
    if (len(polygon_points) > 0):
        cv2.fillPoly(image, np.array([polygon_points]), (255,0,0))

    # And show it
    cv2.imshow("image", image)
    # Waiting for the user to press any key
    cv2.waitKey(0)
    #cv2.destroyWindow("image")
    cv2.destroyAllWindows()



def separate_mask_from_image():

    # Firstly let's save the masked
    def save_masked_image():
        # Save image to path
        global path_to_save_image
        create_project_path()
        
        #if image != all():
            #print("QWERT")
            #print(image)
        split_image = image.copy()
        cv2.imread(path_to_save_image)
        os.chdir(path_to_save_image)
        cv2.imwrite(str(image_number)+".png", split_image)

    try:
        save_masked_image()
    

        global image_masked_path
        image_masked_path = filedialog.askopenfilename()

        
        # open source image file
        #image = cv2.imread('face.jpg', cv2.IMREAD_UNCHANGED)

        global image_masked


        # load the input image and convert it to PIL format
        image_masked = Image.open(image_masked_path)
        image_masked = image_masked.convert("RGB")

        # create a canvas to display the image
        global image_masked_window
        image_masked_window = Toplevel(window)
        image_masked_window.title("Masked Image - Split")
        image_masked_window.grab_set()
        canvas = Canvas(image_masked_window, width=image_masked.width, height=image_masked.height)
        canvas.pack()

        # create a photo image object to display the image on the canvas
        photo = ImageTk.PhotoImage(image_masked)
        canvas.create_image(0, 0, image=photo, anchor=NW)

        # Create new project menu
        image_masked_window_menu = Menu(image_masked_window)
        image_masked_window.config(menu=image_masked_window_menu)

        def quit_split_image_masked():
            image_masked_window.destroy()
            image_masked_window.update()

        # define a function to handle keyboard presses on the window
        def keypress(event):
            # get the key code
            key = event.keycode

            # if the key is Enter (13), apply the mask and split the channels
            if key == 13:
            ####test to change envent from the keyboard to the mouse
            #if event == cv2.EVENT_LBUTTONDOWN:
                # convert the PIL image to OpenCV format
                image_cv = np.array(image_masked)
                image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

                # create a mask with the same size and shape as the image
                mask = np.zeros(image_cv.shape[:2], dtype="uint8")

                # fill the polygon area with white color using the points list
                cv2.fillPoly(mask, [np.array(polygon_points)], 255)

                # apply the mask to the image using bitwise AND operation
                masked = cv2.bitwise_and(image_cv, image_cv, mask=mask)

                # save the masked image as a new file
                cv2.imwrite("masked.png", masked)

                # split the masked image into three channels: blue, green and red
                blue, green, red = cv2.split(masked)

                # save each channel as a separate image file
                cv2.imwrite("blue.png", blue)


                #After pressing the ENTER key & save all files close the window
                quit_split_image_masked()

        # bind the keypress function to any key press on the window
        window.bind("<Key>", keypress)
        #window.bind("<Button-1>", keypress)
        

        # Add new project file menu
        image_masked_menu = Menu(image_masked_window_menu, tearoff=False)
        image_masked_window_menu.add_cascade(label="Project file", menu=image_masked_menu)

        image_masked_menu.add_command(label="Exit", command=quit_split_image_masked)

        # start the main loop of the window
        image_masked_window.mainloop()
    except NameError:
        print("SHAWASKA in 'separate_mask_from_image(): NameError'")
        no_image = "The image was not labeled before. You need to label some image first."
        image_not_labeled_error = Label(window, text=no_image)
        image_not_labeled_error.place(x=20, y=40)



# Add main file menu
file_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Create Project Path", command=create_project_path)
#file_menu.add_command(label="Open Project", command=open_image_and_mask)
file_menu.add_command(label="Open Image to Mask", command=open_image_to_mask)
file_menu.add_command(label="Save & Separate Mask from Image", command=separate_mask_from_image)

file_menu.add_command(label="Exit", command=exit_application)

print(os.path.expanduser('~\Documents'))


# kick off the GUI
window.mainloop()