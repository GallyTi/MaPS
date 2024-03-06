import os
import tkinter as tk
from tkinter import filedialog
import pydicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider

class DicomViewer:
    def __init__(self, master):
        self.master = master
        master.title("DICOM Viewer")
        self.directory_path = ""
        self.images = []
        
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.35)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(master, text="Load DICOM Directory", command=self.load_dicom_directory)
        self.load_button.pack(side=tk.TOP)
        
        self.exit_button = tk.Button(master, text="Exit", command=self.close_application)
        self.exit_button.pack(side=tk.BOTTOM)

        self.slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
        self.slider = Slider(self.slider_ax, 'Index', 0, 1, valinit=0, valstep=1)
        self.slider.on_changed(self.update_image)

        master.protocol("WM_DELETE_WINDOW", self.close_application)

    def load_dicom_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.images = self.load_dicom_images(self.directory_path)
            if self.images:
                self.slider_ax.clear()
                self.slider = Slider(self.slider_ax, 'Index', 0, len(self.images)-1, valinit=0, valstep=1)
                self.slider.on_changed(self.update_image)
                self.update_image(0)
    
    def load_dicom_images(self, directory):
        images = []
        file_names = os.listdir(directory)
        file_paths = [os.path.join(directory, name) for name in file_names if name.endswith('.dcm')]
        for file_path in sorted(file_paths):
            ds = pydicom.dcmread(file_path)
            if hasattr(ds, 'pixel_array'):
                images.append(ds.pixel_array)
        return images

    def update_image(self, index):
        index = int(index)
        if self.images:
            self.ax.clear()
            self.ax.imshow(self.images[index], cmap='gray')
            self.ax.axis('off')
            self.canvas.draw()

    def close_application(self):
        self.master.quit()  # ukončí hlavnú slučku
        self.master.destroy()  # zruší okno

root = tk.Tk()
app = DicomViewer(root)
root.mainloop()