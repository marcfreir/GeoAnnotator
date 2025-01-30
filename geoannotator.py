import sys
import os
import json
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QColorDialog, QLabel, QVBoxLayout, 
    QWidget, QPushButton, QHBoxLayout, QGraphicsView, QGraphicsScene, 
    QGraphicsPixmapItem, QGraphicsPathItem
)
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QEvent
from PIL import Image, ImageDraw
import tifffile

class CustomGraphicsView(QGraphicsView):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Reference to main window
        self.viewport().setCursor(Qt.CrossCursor)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.zoom_factor = 1.25
        self.last_mouse_pos = None
        self.current_path_item = None
        self.current_path = None

        # Set cross cursor
        self.setCursor(Qt.CrossCursor)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_factor, self.zoom_factor)
        else:
            self.scale(1/self.zoom_factor, 1/self.zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            scene_pos = self.mapToScene(event.pos())
            self.main_window.handle_left_press(scene_pos)  # Call main window method
        elif event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.last_mouse_pos:
            scene_pos = self.mapToScene(event.pos())
            self.main_window.handle_left_move(scene_pos)  # Call main window method
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None
            scene_pos = self.mapToScene(event.pos())
            self.main_window.handle_left_release(scene_pos)  # Call main window method
        elif event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.NoDrag)
        super().mouseReleaseEvent(event)

class ImageSegmentationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GeoAnnotator App')
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.statusBar = self.statusBar()
        self.label_counter = 0
        self.log_file_path = None

        # Add menu bar to the main window (QMainWindow)
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)

        # Graphics View
        self.view = CustomGraphicsView(self)
        self.layout.addWidget(self.view)
        self.scene = self.view.scene

        # Buttons layout
        button_layout = QHBoxLayout()
        self.open_button = QPushButton('Open Image')
        self.open_button.clicked.connect(self.open_image)
        button_layout.addWidget(self.open_button)

        self.color_button = QPushButton('Create New Class | Pick Color')
        self.color_button.clicked.connect(self.choose_color)
        button_layout.addWidget(self.color_button)

        self.reset_button = QPushButton('Reset Labels')
        self.reset_button.clicked.connect(self.reset_labels)
        button_layout.addWidget(self.reset_button)

        self.save_button = QPushButton('Save Labels')
        self.save_button.clicked.connect(self.save_labels)
        button_layout.addWidget(self.save_button)

        # Add mask button
        self.save_mask_button = QPushButton('Save Masks')
        self.save_mask_button.clicked.connect(self.save_masks)
        button_layout.addWidget(self.save_mask_button)

        # Class management
        self.class_colors = {}  # {(r,g,b): class_index}
        self.class_names = {}   # {class_index: name}
        self.next_class_index = 1
        self.load_class_mapping()

        self.layout.addLayout(button_layout)

        # Variables
        self.image = None
        self.image_item = None
        self.labels = []
        self.current_label = []
        self.current_color = QColor(255, 0, 0)
        self.drawing = False
        self.current_path_item = None

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)'
        )

        if file_path:
            self.image_path = file_path
            
            # Handle TIFF files differently
            if file_path.lower().endswith(('.tif', '.tiff')):
                try:
                    # Read TIFF using tifffile
                    tiff_img = tifffile.imread(file_path)
                    # Convert numpy array to PIL Image
                    self.image = Image.fromarray(tiff_img).convert('RGB')
                except Exception as e:
                    self.statusBar.showMessage(f"Error opening TIFF: {str(e)}", 5000)
                    return
            else:
                # Handle other formats with PIL
                try:
                    self.image = Image.open(file_path).convert('RGB')
                except Exception as e:
                    self.statusBar.showMessage(f"Error opening image: {str(e)}", 5000)
                    return

            # Rest of the loading logic
            self.scene.clear()
            self.current_label = []
            self.labels = []

            # Convert PIL image to QPixmap
            qimage = QImage(self.image.tobytes(), self.image.width, self.image.height, 
                           self.image.width * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.image_item)
            self.scene.setSceneRect(0, 0, self.image.width, self.image.height)
            self.view.fitInView(self.image_item, Qt.KeepAspectRatio)
            self.statusBar.showMessage(f'Image opened: {file_path}')

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = color

            # Register new color if needed
            rgb = (color.red(), color.green(), color.blue())
            if rgb not in self.class_colors:
                self.class_colors[rgb] = self.next_class_index
                self.class_names[self.next_class_index] = f'Class {self.next_class_index}'
                self.next_class_index += 1
                self.save_class_mapping()

    def save_class_mapping(self):
        mapping = {
            f'{r},{g},{b}': {
                'index': idx,
                'name': self.class_names[idx]
            }
            for (r,g,b), idx in self.class_colors.items()
        }
        with open('class_mapping.json', 'w') as f:
            json.dump(mapping, f, indent=2)

    def load_class_mapping(self):
        try:
            with open('class_mapping.json', 'r') as f:
                mapping = json.load(f)
                for rgb_str, data in mapping.items():
                    r, g, b = map(int, rgb_str.split(','))
                    idx = data['index']
                    self.class_colors[(r,g,b)] = idx
                    self.class_names[idx] = data['name']
                if self.class_colors:
                    self.next_class_index = max(self.class_names.keys()) + 1
        except FileNotFoundError:
            pass

    def save_masks(self):
        if not self.image or not self.labels:
            return
        
        # Create grayscale mask
        mask = Image.new('L', self.image.size, 0)
        draw = ImageDraw.Draw(mask)
        
        # Draw all labels
        for polygon, color in self.labels:
            rgb = (color.red(), color.green(), color.blue())
            class_idx = self.class_colors.get(rgb, 0)
            if class_idx == 0:
                continue  # Skip unregistered colors
                
            points = [(p.x(), p.y()) for p in polygon]
            draw.polygon(points, fill=class_idx)
        
        # Save mask
        base_name = os.path.splitext(os.path.basename(self.image_path))[0]
        default_path = os.path.join(os.path.dirname(self.image_path), f'{base_name}_mask.png')
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Mask', default_path, 'PNG Files (*.png)'
        )
        
        if file_path:
            if not file_path.lower().endswith('.png'):
                file_path += '.png'
            mask.save(file_path)
            self.statusBar.showMessage(f'Mask saved to {file_path}', 3000)

    def handle_left_press(self, scene_pos):
        if self.image:
            x = int(scene_pos.x())
            y = int(scene_pos.y())
            if 0 <= x < self.image.width and 0 <= y < self.image.height:
                self.drawing = True
                self.current_label = [QPoint(x, y)]
                self.current_path = QPainterPath()
                self.current_path.moveTo(x, y)
                self.current_path_item = QGraphicsPathItem(self.current_path)
                self.current_path_item.setPen(QPen(self.current_color, 2))
                self.scene.addItem(self.current_path_item)

    def handle_left_move(self, scene_pos):
        if self.drawing and self.image:
            x = int(scene_pos.x())
            y = int(scene_pos.y())
            if 0 <= x < self.image.width and 0 <= y < self.image.height:
                self.current_label.append(QPoint(x, y))
                self.current_path.lineTo(x, y)
                self.current_path_item.setPath(self.current_path)

    def handle_left_release(self, scene_pos):
        if self.drawing:
            self.drawing = False
            # Check if right-click to close polygon
            if len(self.current_label) > 2:
                self.current_label.append(self.current_label[0])
                self.current_path.lineTo(self.current_label[0].x(), self.current_label[0].y())
                self.current_path_item.setPath(self.current_path)
                self.fill_label()

    def fill_label(self):
        if self.image and self.current_label:
            polygon = [(p.x(), p.y()) for p in self.current_label]
            mask = Image.new('L', self.image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.polygon(polygon, fill=255)

            color_layer = Image.new('RGBA', self.image.size, self.current_color.name())
            overlay = Image.alpha_composite(self.image.convert('RGBA'), color_layer.convert('RGBA'))
            overlay.putalpha(mask)

            qimage = QImage(overlay.tobytes(), overlay.width, overlay.height, 
                            overlay.width * 4, QImage.Format_RGBA8888)
            overlay_item = QGraphicsPixmapItem(QPixmap.fromImage(qimage))
            self.scene.addItem(overlay_item)
            self.labels.append((self.current_label, self.current_color))
            self.save_label_log()

            label_name = ['First', 'Second', 'Third', 'Fourth', 'Fifth']
            nth_label = label_name[self.label_counter] if self.label_counter < len(label_name) else f'{self.label_counter + 1}th'
            self.statusBar.showMessage(f'{nth_label} label created successfully!', 3000)
            self.label_counter += 1

    def reset_labels(self):
        self.scene.clear()
        if self.image:
            qimage = QImage(self.image.tobytes(), self.image.width, self.image.height, 
                           self.image.width * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.image_item)
        self.labels = []
        self.label_counter = 0

    def save_label_log(self):
        if not self.image or not self.labels:
            return
        image_name = os.path.splitext(os.path.basename(self.image_path))[0]
        log_dir = f'{image_name}_logs'
        os.makedirs(log_dir, exist_ok=True)
        self.log_file_path = os.path.join(log_dir, f'{image_name}_log.txt')
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f'\nLabel_{self.label_counter}:\n')
            for point in self.current_label:
                log_file.write(f'({point.x()}, {point.y()})\n')
        self.statusBar.showMessage(f'Label {self.label_counter} saved!', 3000)

    def save_labels(self):
        if self.image:
            file_path, _ = QFileDialog.getSaveFileName(
                self, 'Save Labels', '', 'PNG Files (*.png)'
            )
            if file_path:
                # Ensure the filename ends with .png
                if not file_path.lower().endswith('.png'):
                    file_path += '.png'
                
                # Create white background with labels
                white_bg = Image.new('RGBA', self.image.size, (255, 255, 255, 255))
                for label in self.labels:
                    polygon, color = label
                    mask = Image.new('L', self.image.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.polygon([(p.x(), p.y()) for p in polygon], fill=255)
                    color_layer = Image.new('RGBA', self.image.size, color.name())
                    white_bg.paste(color_layer, mask=mask)
                
                # Convert to RGB before saving to avoid alpha channel issues
                white_bg.convert('RGB').save(file_path)
                self.statusBar.showMessage(f'Labels saved as {file_path}', 3000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSegmentationApp()
    window.show()
    sys.exit(app.exec_())