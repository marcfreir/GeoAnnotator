import cv2
import numpy as np
import tkinter as tk
from tkinter import simpledialog

def get_label_name():
    root = tk.Tk()
    root.withdraw()

    label_name = simpledialog.askstring("Label Name", "Enter a label for the new polygon mask:")
    return label_name

def draw_polygon(image_path):
    # Initialize the flag for polygon drawing
    drawing_polygon = False
    points = []
    annotations = []
    undo_stack = []

    # Initialize the color dictionary for labels
    label_colors = {
        "label1": (0, 255, 0),  # Green
        "label2": (0, 0, 255),  # Red
        "label3": (255, 0, 0)   # Blue
    }

    # Create a callback function for mouse events
    def draw_polygon(event, x, y, flags, param):
        nonlocal drawing_polygon, points

        # Left mouse button is pressed
        if event == cv2.EVENT_LBUTTONDOWN:
            # Start drawing the polygon
            drawing_polygon = True
            points.append((x, y))

        # Mouse is being moved with the left button pressed
        elif event == cv2.EVENT_MOUSEMOVE and drawing_polygon:
            # Update the last point of the polygon
            points[-1] = (x, y)

        # Left mouse button is released
        elif event == cv2.EVENT_LBUTTONUP:
            # Finish drawing the polygon
            drawing_polygon = False
            points.append((x, y))

    # Load the image
    image = cv2.imread(image_path)

    # Create a window and bind the callback function to it
    cv2.namedWindow("GeoAnnotator - Image Annotation")
    cv2.setMouseCallback("GeoAnnotator - Image Annotation", draw_polygon)

    label = ""  # Initialize label variable

    while True:
        # Display the image with the lines connecting the points
        temp_image = image.copy()
        if len(points) > 0 and not drawing_polygon:
            cv2.polylines(temp_image, [np.array(points)], isClosed=False, color=(0, 0, 0), thickness=2)
            for point in points:
                cv2.circle(temp_image, point, radius=2, color=(0, 255, 0), thickness=-1)

        cv2.imshow("GeoAnnotator - Image Annotation", temp_image)

        # Wait for key press
        key = cv2.waitKey(1) & 0xFF

        # Finish the current polygon and prompt for label
        if key == ord('d'):
            if len(points) > 0:
                # Prompt for label
                label = get_label_name()
                annotations.append((list(points), label))
                points = []

        # Undo the last point
        elif key == ord('u'):
            if len(points) > 0:
                points.pop()

        # Exit if the 'Esc' key is pressed
        elif key == 27:
            break

    # Create separate masks for each label
    masks = {}
    for points, label in annotations:
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [np.array(points)], 1)
        if label in masks:
            masks[label] = cv2.bitwise_or(masks[label], mask)
        else:
            masks[label] = mask

        # Save the points as a text file for the current mask
        points_file = open(f"{label}_points.txt", "w")
        points_str = '[' + ', '.join([f"({p[0]}, {p[1]})" for p in points]) + ']'
        points_file.write(points_str)
        points_file.close()

    # Save the masks as binary images
    for label, mask in masks.items():
        cv2.imwrite(f"{label}_mask.png", mask * 255)

    # Close the window
    cv2.destroyAllWindows()
