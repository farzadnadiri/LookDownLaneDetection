import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import cv2
from hsv_controls import create_hsv_controls, save_hsv_values, load_hsv_values, reset_hsv_values, get_hsv_min_values, get_hsv_max_values
from video_controls import update_all_frames

def log_message(textbox, message):
    textbox.insert(tk.END, message + "\n")
    textbox.see(tk.END)

# Log function to pass to processing functions
def log_func(message):
    log_message(log_console, message)

# Window setup
window = tk.Tk()
window.title("Lane Detection using Look Down Method")
window.geometry('1330x720')

# Video capture object
cap = cv2.VideoCapture('sample.mp4')
# Video frames and labels
frame1 = ttk.Label(window)
frame1.place(x=10, y=10, width=320, height=240)
label1 = ttk.Label(window, text="Original Frame")
label1.place(x=10, y=250, width=320, height=20)

frame2 = ttk.Label(window)
frame2.place(x=340, y=10, width=320, height=240)
label2 = ttk.Label(window, text="Convex Hull")
label2.place(x=340, y=250, width=320, height=20)

frame3 = ttk.Label(window)
frame3.place(x=670, y=10, width=320, height=240)
label3 = ttk.Label(window, text="Masked Lines")
label3.place(x=670, y=250, width=320, height=20)

frame4 = ttk.Label(window)
frame4.place(x=1000, y=10, width=320, height=240)
label4 = ttk.Label(window, text="Detected Lines")
label4.place(x=1000, y=250, width=320, height=20)

# Distance label
distance_label = ttk.Label(window, text="Distance to lane: ")
distance_label.place(x=10, y=280, width=1280, height=20)

# Log console
log_console = ScrolledText(window, height=10)
log_console.place(x=10, y=510, width=1320, height=200)

# Radio buttons for Lane and Road selection
mode_selection = tk.StringVar(value="Lane")
lane_radio = ttk.Radiobutton(window, text="Lane", variable=mode_selection, value="Lane")
lane_radio.place(x=600, y=320)
road_radio = ttk.Radiobutton(window, text="Road", variable=mode_selection, value="Road")
road_radio.place(x=600, y=350)

# Create HSV controls and buttons
create_hsv_controls(window, log_func)

save_button = ttk.Button(window, text="Save", command=lambda:
                         save_hsv_values(log_func, mode_selection))
save_button.place(x=600, y=380, width=100, height=30)

load_button = ttk.Button(window, text="Load", command=lambda:
                         load_hsv_values(log_func, mode_selection))
load_button.place(x=600, y=420, width=100, height=30)

reset_button = ttk.Button(window, text="Reset", command=lambda: reset_hsv_values(log_func))
reset_button.place(x=600, y=460, width=100, height=30)

# Function to repeatedly call update_all_frames
def schedule_update():
    update_all_frames(cap, frame1, frame2, frame3, frame4, log_func, distance_label, get_hsv_min_values(), get_hsv_max_values())
    window.after(10, schedule_update)

# Start the initial frame update and schedule recurring updates
schedule_update()

# Apply reset at start
reset_hsv_values(log_func)

# Log the startup
log_message(log_console, "Application started with default HSV values.")

# Run the application
window.mainloop()

# Release video capture object
cap.release()
