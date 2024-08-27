import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import cv2
from hsv_controls import create_hsv_controls, save_hsv_values, load_hsv_values, reset_hsv_values, get_hsv_min_values, get_hsv_max_values, get_erode_size, get_dilate_size
from video_controls import update_all_frames
# Import Matplotlib modules for embedding
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def log_message(textbox, message):
    textbox.insert(tk.END, message + "\n")
    textbox.see(tk.END)

def log_func(message):
    log_message(log_console, message)

# Window setup
window = tk.Tk()
window.title("Lane Detection using Look Down Method")
window.geometry('1900x1550')  # Adjusted height for better layout

# Video capture objects for left and right cameras
cap_left = cv2.VideoCapture('sample_left.mp4')
cap_right = cv2.VideoCapture('sample_right.mp4')

# Function to create video frames and labels dynamically
def create_frame_and_label(x, y, text):
    frame = ttk.Label(window)
    frame.place(x=x, y=y, width=320, height=240)
    label = ttk.Label(window, text=text)
    label.place(x=x, y=y+250, width=320, height=20)
    return frame, label

def create_histogram(parent, data):
    # Ensure data is 1D
    data = np.ravel(data)  # Use np.ravel() to flatten any multi-dimensional array to 1D
    
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.hist(data, bins=30, color='blue', alpha=0.7)
    
    # Embed Matplotlib figure into Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().place(x=1400, y=10, width=400, height=300)  # Position it as needed
    return canvas

# Create frames for the left camera
left_frame1, left_label1 = create_frame_and_label(10, 10, "Original Frame (Left)")
left_frame2, left_label2 = create_frame_and_label(340, 10, "Convex Hull (Left)")
left_frame3, left_label3 = create_frame_and_label(10, 300, "Masked Lines (Left)")
left_frame4, left_label4 = create_frame_and_label(340, 300, "Detected Lines (Left)")

# Create frames for the right camera
right_frame1, right_label1 = create_frame_and_label(700, 10, "Original Frame (Right)")
right_frame2, right_label2 = create_frame_and_label(1030, 10, "Convex Hull (Right)")
right_frame3, right_label3 = create_frame_and_label(700, 300, "Masked Lines (Right)")
right_frame4, right_label4 = create_frame_and_label(1030, 300, "Detected Lines (Right)")

# Distance labels for both cameras
distance_label_left = ttk.Label(window, text="Distance to lane (Left): ")
distance_label_left.place(x=10, y=580, width=300, height=20)

alg_selection_left = tk.StringVar(value="hough")
left_hough_radio = ttk.Radiobutton(window, text="hough transform", variable=alg_selection_left, value="hough")
left_hough_radio.place(x=250, y=580)
left_sliding_radio = ttk.Radiobutton(window, text="sliding window", variable=alg_selection_left, value="sliding")
left_sliding_radio.place(x=400, y=580)

distance_label_right = ttk.Label(window, text="Distance to lane (Right): ")
distance_label_right.place(x=700, y=580, width=300, height=20)

alg_selection_right = tk.StringVar(value="hough")
right_hough_radio = ttk.Radiobutton(window, text="hough transform", variable=alg_selection_right, value="hough")
right_hough_radio.place(x=950, y=580)
right_sliding_radio = ttk.Radiobutton(window, text="sliding window", variable=alg_selection_right, value="sliding")
right_sliding_radio.place(x=1100, y=580)

# Radio buttons for Lane and Road selection for both cameras
mode_selection_left = tk.StringVar(value="Lane")
mode_selection_right = tk.StringVar(value="Lane")

left_lane_radio = ttk.Radiobutton(window, text="Lane", variable=mode_selection_left, value="Lane")
left_lane_radio.place(x=10, y=620)
left_road_radio = ttk.Radiobutton(window, text="Road", variable=mode_selection_left, value="Road")
left_road_radio.place(x=70, y=620)

right_lane_radio = ttk.Radiobutton(window, text="Lane", variable=mode_selection_right, value="Lane")
right_lane_radio.place(x=700, y=620)
right_road_radio = ttk.Radiobutton(window, text="Road", variable=mode_selection_right, value="Road")
right_road_radio.place(x=770, y=620)

# Create HSV controls and buttons for the left camera
create_hsv_controls(window, log_func, "Left", x_offset=30, y_offset=680)

save_button_left = ttk.Button(window, text="Save Left", command=lambda: save_hsv_values(log_func, mode_selection_left, "Left"))
save_button_left.place(x=140, y=615, width=100, height=30)

load_button_left = ttk.Button(window, text="Load Left", command=lambda: load_hsv_values(log_func, mode_selection_left, "Left"))
load_button_left.place(x=250, y=615, width=100, height=30)

reset_button_left = ttk.Button(window, text="Reset Left", command=lambda: reset_hsv_values(log_func, "Left"))
reset_button_left.place(x=360, y=615, width=100, height=30)

# Create HSV controls and buttons for the right camera
create_hsv_controls(window, log_func, "Right", x_offset=720, y_offset=680)

save_button_right = ttk.Button(window, text="Save Right", command=lambda: save_hsv_values(log_func, mode_selection_right, "Right"))
save_button_right.place(x=840, y=615, width=100, height=30)

load_button_right = ttk.Button(window, text="Load Right", command=lambda: load_hsv_values(log_func, mode_selection_right, "Right"))
load_button_right.place(x=950, y=615, width=100, height=30)

reset_button_right = ttk.Button(window, text="Reset Right", command=lambda: reset_hsv_values(log_func, "Right"))
reset_button_right.place(x=1060, y=615, width=100, height=30)


# Log console
log_console = ScrolledText(window, height=10)
log_console.place(x=10, y=870, width=1340, height=150)


# Function to repeatedly call update_all_frames
def schedule_update():
    historgramLeft = update_all_frames(cap_left, left_frame1, left_frame2, left_frame3, left_frame4, log_func, distance_label_left,
                      get_hsv_min_values("Left"), get_hsv_max_values("Left"), get_erode_size("Left"), get_dilate_size("Left"),"Left",alg_selection_left.get())
    update_all_frames(cap_right, right_frame1, right_frame2, right_frame3, right_frame4, log_func, distance_label_right,
                      get_hsv_min_values("Right"), get_hsv_max_values("Right"), get_erode_size("Right"), get_dilate_size("Right"),"Right",alg_selection_right.get())
    
    window.after(10, schedule_update)

# Start the initial frame update and schedule recurring updates
schedule_update()

# Apply reset at start for both cameras
reset_hsv_values(log_func, "Left")
reset_hsv_values(log_func, "Right")

# Log the startup
log_message(log_console, "Application started with default HSV values.")

# Run the application
window.mainloop()

# Release video capture objects
cap_left.release()
cap_right.release()
