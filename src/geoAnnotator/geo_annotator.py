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

##### Create OS path to save image #####
# Create path on OS
path_to_save_image = "../geoAnnotator/RESULT_DRAW_POLYGON"
# Check if path already exists
if not os.path.exists(path_to_save_image):
    os.mkdir(path_to_save_image)
    
print("Directory '% s' created" % path_to_save_image)


################### TO DRAW POLYGON ON IMAGE - BEGIN ##########

# ***** global variable declaration *****
done = False
points = []
current = (0,0)
prev_current = (0,0)
img_number = 0

################### TO DRAW POLYGON ON IMAGE - END ##########


####MAYBE DO NOT SHOW THE TKINTER TOP LEVEL, INSTEAD SHOW DIRECTLY THE CV2 "NAMEDWINDOW"
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


    # Open image
    def open_image():

        global panel_image
        # Open a file chooser dialog and allow the user to select an input
        # Image
        img_path = filedialog.askopenfilename()

        
        global image_to_open
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


                new_image = cv2.imread(img_path)
                image_clone = new_image.copy()
                image_temp = new_image.copy()

                def on_mouse(event, x, y, buttons, user_param):
                    global done, points, current,image_temp
                    # Mouse callback that gets called for every mouse event (i.e. moving, clicking, etc.)
                    if done: # Nothing more to do
                        return
                    if event == cv2.EVENT_MOUSEMOVE:
                        # We want to be able to draw the line-in-progress, so update current mouse position
                        current = (x, y)
                    elif event == cv2.EVENT_LBUTTONDOWN:
                        # Left click means adding a point at current position to the list of points
                        print("Adding point #%d with position(%d,%d)" % (len(points), x, y))
                        cv2.circle(new_image,(x,y),5,(0,200,0),-1)
                        points.append([x, y])
                        image_temp = new_image.copy()
                    elif event == cv2.EVENT_RBUTTONDOWN:
                        # Right click means we're done
                        print("Completing polygon with %d points." % len(points))
                        done = True

                cv2.namedWindow("image")
                cv2.setMouseCallback("image", on_mouse)

                
                global done
                #done = False
                while(not done):
                    # This is our drawing loop, we just continuously draw new images
                    # and show them in the named window
                    if (len(points) > 1):
                        if(current != prev_current):
                            new_image = image_temp.copy()
                        # Draw all the current polygon segments
                        cv2.polylines(new_image, [np.array(points)], False, (255,0,0), 1)
                        # And  also show what the current segment would look like
                        cv2.line(new_image, (points[-1][0],points[-1][1]), current, (255,0,255))

                    # --->>> Create a new thread for the instanciated window <<<<-----
                    cv2.startWindowThread()
                    # Update the window
                    cv2.imshow("image", new_image)
                    # And wait 50ms before next iteration (this will pump window messages meanwhile)

                    if cv2.waitKey(50) == ord('d'): # press d(done)
                        done = True
                        

                # User finised entering the polygon points, so let's make the final drawing
                new_image = image_clone.copy()
                # of a filled polygon
                if (len(points) > 0):
                    cv2.fillPoly(new_image, np.array([points]), (255,0,0))
                # And show it
                cv2.imshow("image", new_image)

                # Save the image drawn on canvas
                #def save_image():
                #image_to_save = new_image.copy()
                #cv2.imread(path_to_save_image)
                #os.chdir(path_to_save_image)
                #cv2.imwrite(str(img_number)+".png",image_to_save)

                global image_to_save
                image_to_save = new_image.copy()
                

                # Waiting for the user to press any key
                cv2.waitKey(0)
                #cv2.destroyWindow("image")
                cv2.destroyAllWindows()


            else:
                # update the panel
                panel_image.configure(image=image_to_open)
                panel_image.image_to_open = image_to_open


# initialize the image panels
#panel_image = None


    # Add new project file menu
    new_project_menu = Menu(new_project_window_menu, tearoff=False)
    new_project_window_menu.add_cascade(label="Project file", menu=new_project_menu)
    new_project_menu.add_command(label="Save this project", command=save_image)
    new_project_menu.add_command(label="Open image in project", command=open_image)
    new_project_menu.add_command(label="Exit", command=exit_new_project)
    

panel_image = None

def create_new_project():
    new_project_window()

def open_project():
    pass

def save_project():
    pass

def save_image():
    #image_to_save = new_image.copy()
    cv2.imread(path_to_save_image)
    os.chdir(path_to_save_image)
    cv2.imwrite(str(img_number)+".png",image_to_save)

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