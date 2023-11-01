import sys
import math
import OpenGL.GL as gl
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QPushButton, QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QSplitter


class OpenGLWidget(QOpenGLWidget):
    def _init_(self):
        super()._init_()
        self.vertices = []
        self.primitive = "Point"
        self.grid_rows = 1
        self.grid_cols = 1
        self.line_width = 5
        self.is_drawing = False
        self.shape_color = (0.0, 0.0, 1.0)

    def setLineWidth(self, value):
        self.line_width = value
        gl.glLineWidth(self.line_width)
        gl.glPointSize(self.line_width)
        self.update()

    def startDrawing(self):
        self.is_drawing = True
        self.vertices = []
        self.update()

    def stopDrawing(self):
        self.is_drawing = False

    def initializeGL(self):
        gl.glClearColor(0.95, 0.95, 0.95, 1)
        gl.glPointSize(self.line_width)
        gl.glLineWidth(self.line_width)

    def setColor(self):
        color_dialog = QColorDialog(self)
        new_color = color_dialog.getColor(initial=Qt.red)
        if new_color.isValid():
            self.shape_color = (
                new_color.red() / 255.0, new_color.green() / 255.0, new_color.blue() / 255.0)
            self.update()

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glColor3f(0, 0, 0)
        self.drawGrid()

        if self.primitive == "Point":
            self.drawPoints()
        elif self.primitive == "Line":
            self.drawLines()
        elif self.primitive == "Polygon":
            self.drawPolygon()
        elif self.primitive == "Circle":
            self.drawCircle()
        elif self.primitive == "Ellipse":
            self.drawEllipse()

    def drawGrid(self):
        step_x = 2 / self.grid_cols
        step_y = 2 / self.grid_rows
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(0.7, 0.7, 0.7)
        for i in range(-self.grid_cols, self.grid_cols + 1):
            x = i * step_x
            gl.glVertex2f(x, -1)
            gl.glVertex2f(x, 1)
        for i in range(-self.grid_rows, self.grid_rows + 1):
            y = i * step_y
            gl.glVertex2f(-1, y)
            gl.glVertex2f(1, y)
        gl.glEnd()

    def drawPoints(self):
        gl.glBegin(gl.GL_POINTS)
        gl.glColor3f(*self.shape_color)
        for vertex in self.vertices:
            gl.glVertex2fv(vertex)
        gl.glEnd()

    def drawLines(self):
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(*self.shape_color)
        for i in range(0, len(self.vertices) - 1, 2):
            if i + 1 < len(self.vertices):
                gl.glVertex2fv(self.vertices[i])
                gl.glVertex2fv(self.vertices[i + 1])
        gl.glEnd()

    def drawPolygon(self):
        gl.glBegin(gl.GL_POLYGON)
        gl.glColor3f(*self.shape_color)
        for vertex in self.vertices:
            gl.glVertex2fv(vertex)
        gl.glEnd()

    def drawCircle(self):
        if len(self.vertices) == 2:
            center = self.vertices[0]
            radius = math.dist(center, self.vertices[1])
            num_segments = 100
            aspect_ratio = self.width() / self.height()
            angle = 2 * math.pi / num_segments
            gl.glBegin(gl.GL_LINE_LOOP)
            gl.glColor3f(*self.shape_color)
            for i in range(num_segments):
                x = center[0] + radius * math.cos(i * angle)
                y = center[1] + radius * math.sin(i * angle) * aspect_ratio
                gl.glVertex2f(x, y)
            gl.glEnd()

    def drawEllipse(self):
        if len(self.vertices) == 2:
            center = self.vertices[0]
            radius_x = math.dist(center, self.vertices[1])
            radius_y = radius_x
            num_segments = 100
            angle = 2 * math.pi / num_segments
            gl.glBegin(gl.GL_LINE_LOOP)
            gl.glColor3f(*self.shape_color)
            for i in range(num_segments):
                x = center[0] + radius_x * math.cos(i * angle)
                y = center[1] + radius_y * math.sin(i * angle)
                gl.glVertex2f(x, y)
            gl.glEnd()

    def mousePressEvent(self, event):
        if self.is_drawing:
            x = event.x()
            y = event.y()
            x = (x / self.width()) * 2 - 1
            y = 1 - (y / self.height()) * 2
            self.vertices.append((x, y))
            self.update()


class MainWindow(QMainWindow):
    def _init_(self):
        super()._init_()

        self.setWindowTitle("OpenGL Primitives")
        self.setGeometry(100, 100, 800, 600)

        self.opengl_widget = OpenGLWidget()

        layout_options_widget = QWidget()
        layout_options_layout = QVBoxLayout()

        button_style = "QPushButton { background-color: white; font-size: 25px; color: black; border: 2px solid #005299; border-radius: 7px; padding: 7px; }" \
            "QPushButton:hover { background-color: #005DA1; color: white; }"

        self.primitive_combobox = QComboBox()
        self.primitive_combobox.addItems(
            ["Point", "Line", "Polygon", "Circle", "Ellipse"])
        self.primitive_combobox.activated[str].connect(self.setPrimitive)

        self.primitive_combobox.setStyleSheet(
            "QComboBox { background-color: black; font-size: 30px; border: 5px solid #ccc; border-radius: 7px; padding: 7px; color: white; }")
        self.primitive_combobox.view().setStyleSheet(
            "QListView { background-color: black; color: white; border: 3px solid #ccc; selection-background-color: #0078D7; }")

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(button_style)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(button_style)
        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.setStyleSheet(button_style)
        self.remove_row_button = QPushButton("Remove Row")
        self.remove_row_button.setStyleSheet(button_style)
        self.add_col_button = QPushButton("Add Column")
        self.add_col_button.setStyleSheet(button_style)
        self.remove_col_button = QPushButton("Remove Column")
        self.remove_col_button.setStyleSheet(button_style)

        self.start_button.clicked.connect(self.opengl_widget.startDrawing)
        self.stop_button.clicked.connect(self.opengl_widget.stopDrawing)
        self.add_row_button.clicked.connect(self.addGridRow)
        self.remove_row_button.clicked.connect(self.removeGridRow)
        self.add_col_button.clicked.connect(self.addGridColumn)
        self.remove_col_button.clicked.connect(self.removeGridColumn)

        layout_options_layout.addWidget(self.primitive_combobox)
        layout_options_layout.addWidget(self.start_button)
        layout_options_layout.addWidget(self.stop_button)
        layout_options_layout.addWidget(self.add_row_button)
        layout_options_layout.addWidget(self.remove_row_button)
        layout_options_layout.addWidget(self.add_col_button)
        layout_options_layout.addWidget(self.remove_col_button)
        layout_options_widget.setLayout(layout_options_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.opengl_widget)
        splitter.addWidget(layout_options_widget)
        splitter.setSizes([3 * self.width() // 4, self.width() // 4])

        self.setCentralWidget(splitter)

    def setPrimitive(self, text):
        self.opengl_widget.primitive = text
        self.opengl_widget.update()

    def removeGridRow(self):
        if self.opengl_widget.grid_rows > 1:
            self.opengl_widget.grid_rows -= 1
            self.opengl_widget.update()

    def removeGridColumn(self):
        if self.opengl_widget.grid_cols > 1:
            self.opengl_widget.grid_cols -= 1
            self.opengl_widget.update()

    def addGridRow(self):
        self.opengl_widget.grid_rows += 1
        self.opengl_widget.update()

    def addGridColumn(self):
        self.opengl_widget.grid_cols += 1
        self.opengl_widget.update()


if _name_ == "_main_":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
