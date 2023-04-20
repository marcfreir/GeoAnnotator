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
    

#def create_new_project():
    #pass

##### Create OS path to save image #####
def create_project_path():
    # Create path on OS
    global path_to_save_image
    path_to_save_image = "./src/geoAnnotator/lab_test/GeoAnnotator/src/RESULT_SCRATCH"

    # Check if path already exists
    if not os.path.exists(path_to_save_image):
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




##############################################################

#def open_project():

opened_image = False

def open_image_to_mask():
    global image_path
    image_path = filedialog.askopenfilename()

    """
    try:
        global image
        image = cv2.imread(image_path)

        #if image is None:
            #print("Shakalakawaka")
        #else:
            #try:
        global image_clone
        image_clone = image.copy()
        global image_temp
        image_temp = image.copy()
            #except NameError:
                #print("Nutika")
    except AttributeError:
        global error
        error = True
        print("Nutika")
    
    """

    
    if image_path is None:
        return 0
    else:
        global image
        image = cv2.imread(image_path)

        #if image is None:
            #print("Shakalakawaka")
        #else:
            #try:
        if image is None:
            return
        else:
            global image_clone
            image_clone = image.copy()
            global image_temp
            image_temp = image.copy()




    # Global variables to draw polygon on selected image
    global done
    done = False
    global polygon_points
    polygon_points = []
    global current_polygon_point
    current_polygon_point = (0,0)
    global prev_current_point
    prev_current_point = (0,0)
    global image_number
    image_number = 0



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
            #set_of_points_file = np.array(set_of_points)
            #global set_of_points_file_read
            set_of_points_file_path = ("./src/geoAnnotator/lab_test/GeoAnnotator/src/RESULT_SCRATCH/set_of_points.txt")
            set_of_points_file = open(set_of_points_file_path,"w")
            add_set_of_points = repr(set_of_points)
            set_of_points_file.write(add_set_of_points)
            set_of_points_file.close

            #set_of_points_file_read = set_of_points_file_path

            """
            from numpy import loadtxt
            lines = loadtxt(set_of_points_file_path)
            print("Shawaska", lines)
            """

            
            #np.savetxt("set_of_points" + str(image_number), set_of_points_file)
            #print("File = ", set_of_points_file)
            # Displaying the contents of the text file
            #content = np.loadtxt('set_of_points0.txt')
            #print("\nContent in file2.txt:\n", content)

            image_temp = image.copy()
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click means we're done
            print("Completing polygon with %d points." % len(polygon_points))
            done = True

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_mouse)

#def test_while():
#open_project()
#global done
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

#test_while()

"""
def save_masked_image():
    # Save image to path
    global path_to_save_image
    create_project_path()
    split_image = image.copy()
    cv2.imread(path_to_save_image)
    os.chdir(path_to_save_image)
    cv2.imwrite(str(image_number)+".png", split_image)
"""

"""
    global image_masked
    image_masked = cv2.imread(image_masked_path, cv2.IMREAD_UNCHANGED)
    #image_masked = cv2.imread("./test/TEST_CVAT_UBUNTU/SegmentationClass/photo_2022-09-28_22-17-49.png")
    gray = cv2.cvtColor(image_masked, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    colors = np.where(hist>5000)
    image_number = 0

    for color in colors[0]:
        print(color)
        split_image = image_masked.copy()
        split_image[np.where(gray != color)] = 0
        cv2.imwrite(str(image_number)+".png", split_image)
        image_number+=1
"""



"""
def separate_mask_from_image():


    global image_masked_path
    image_masked_path = filedialog.askopenfilename()

    
    # open source image file
    #image = cv2.imread('face.jpg', cv2.IMREAD_UNCHANGED)
    global image_masked
    image_masked = cv2.imread(image_masked_path, cv2.IMREAD_UNCHANGED)

    # convert image to grayscale
    image_gray = cv2.cvtColor(image_masked, cv2.COLOR_BGR2GRAY)

    # onvert image to blck and white
    thresh, image_edges = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)

    # create canvas
    canvas = np.zeros(image_masked.shape, np.uint8)
    canvas.fill(255)

    # create background mask
    mask = np.zeros(image_masked.shape, np.uint8)
    mask.fill(255)

    # create new background
    new_background = np.zeros(image_masked.shape, np.uint8)
    new_background.fill(255)

    # get all contours
    contours_draw, hierachy = cv2.findContours(image_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # get most significant contours
    contours_mask, hierachy = cv2.findContours(image_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # draw all contours
    #cv2.drawContours(canvas, contours_draw, 1, (0, 0, 0), 3)

    # contours traversal
    for contour in range(len(contours_draw)):
        # draw current contour
        cv2.drawContours(canvas, contours_draw, contour, (0, 0, 0), 3)

    # most significant contours traversal
    for contour in range(len(contours_mask)):
        # create mask
        if contour != 1:
            cv2.fillConvexPoly(mask, contours_mask[contour], (0, 0, 0))

        # create background
        if contour != 1:
            cv2.fillConvexPoly(new_background, contours_mask[contour], (0, 255, 0))

    # display the image in a window
    cv2.imshow('Original', image_masked)
    cv2.imshow('Contours', canvas)
    cv2.imshow('Background mask', mask)
    cv2.imshow('New background', new_background)
    cv2.imshow('Output', cv2.bitwise_and(image_masked, new_background))

    # write images
    cv2.imwrite('contours.png', canvas)
    cv2.imwrite('mask.png', mask)
    cv2.imwrite('background.png', new_background)
    cv2.imwrite('output.png', cv2.bitwise_and(image_masked, new_background))

    # escape condition
    cv2.waitKey(0)

    # clean up windows
    cv2.destroyAllWindows()

"""

"""
def set_of_points_mask():
    #global set_of_points_file_path
    with open(set_of_points_file_read, "r") as file:
        set_of_points_file_read_f = file.read()
        #text = f.read()
        #text_list = eval(text)
        print("Cowabanga = ", set_of_points_file_read_f)
"""



def separate_mask_from_image():

    # Firstly let's save the masked
    def save_masked_image():
        # Save image to path
        global path_to_save_image
        create_project_path()
        split_image = image.copy()
        cv2.imread(path_to_save_image)
        os.chdir(path_to_save_image)
        cv2.imwrite(str(image_number)+".png", split_image)

    save_masked_image()

    global image_masked_path
    image_masked_path = filedialog.askopenfilename()

    
    # open source image file
    #image = cv2.imread('face.jpg', cv2.IMREAD_UNCHANGED)

    global image_masked
    #image_masked = cv2.imread(image_masked_path, cv2.IMREAD_UNCHANGED)

    ####test#####
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
    
    #############################

    # define a function to handle keyboard presses on the window
    def keypress(event):
        # get the key code
        key = event.keycode

        # if the key is Enter (13), apply the mask and split the channels
        if key == 13:
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
            #blue = cv2.split(masked)

            # save each channel as a separate image file
            cv2.imwrite("blue.png", blue)
            #cv2.imwrite("green.png", green)
            #cv2.imwrite("red.png", red)

    # bind the keypress function to any key press on the window
    window.bind("<Key>", keypress)

    #############################

    # Add new project file menu
    image_masked_menu = Menu(image_masked_window_menu, tearoff=False)
    image_masked_window_menu.add_cascade(label="Project file", menu=image_masked_menu)
    #image_masked_menu.add_command(label="Save this project", command=save_image)
    #image_masked_menu.add_command(label="Open image in project", command=open_image)
    image_masked_menu.add_command(label="Exit", command=quit_split_image_masked)

     # start the main loop of the window
    image_masked_window.mainloop()
    ####test#####
    
    """
    #image_masked = cv2.imread("./test/TEST_CVAT_UBUNTU/SegmentationClass/photo_2022-09-28_22-17-49.png")
    gray = cv2.cvtColor(image_masked, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    colors = np.where(hist>5000)
    image_number = 0

    for color in colors[0]:
        print(color)
        split_image = image_masked.copy()
        split_image[np.where(gray != color)] = 0
        cv2.imwrite(str(image_number)+".png", split_image)
        image_number+=1

    plt.hist(gray.ravel(),256,[0,256])
    plt.savefig('plt')
    plt.show()
    """

# Add main file menu
file_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Create Project Path", command=create_project_path)
#file_menu.add_command(label="Open Project", command=open_image_and_mask)
file_menu.add_command(label="Open Image to Mask", command=open_image_to_mask)
file_menu.add_command(label="Save & Separate Mask from Image", command=separate_mask_from_image)
#file_menu.add_command(label="Mask Image", command=super_function_open_and_mask)
#file_menu.add_command(label="Save", command=save_masked_image)
#file_menu.add_command(label="set_of_points_mask", command=set_of_points_mask)
file_menu.add_command(label="Exit", command=exit_application)

print(os.path.expanduser('~\Documents'))




################### TO DRAW POLYGON ON IMAGE - BEGIN ##########



################### TO DRAW POLYGON ON IMAGE - END ##########



# kick off the GUI
window.mainloop()