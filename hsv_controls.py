import tkinter as tk
from tkinter import ttk
import json
import numpy as np

# Trackbar and value variables
h_min_value = None
h_max_value = None
s_min_value = None
s_max_value = None
v_min_value = None
v_max_value = None
erode_size = None
dilate_size = None

def create_hsv_controls(window, log_func):
    global h_min_value, h_max_value, s_min_value, s_max_value, v_min_value, v_max_value, erode_size, dilate_size
    global h_min_trackbar, h_max_trackbar, s_min_trackbar, s_max_trackbar, v_min_trackbar, v_max_trackbar

    # Initialize the tk.StringVar variables now that we have a root window
    h_min_value = tk.StringVar(value="0")
    h_max_value = tk.StringVar(value="255")
    s_min_value = tk.StringVar(value="0")
    s_max_value = tk.StringVar(value="255")
    v_min_value = tk.StringVar(value="0")
    v_max_value = tk.StringVar(value="255")
    erode_size = tk.StringVar(value="3")
    dilate_size = tk.StringVar(value="1")

    h_min_label = ttk.Label(window, text="Hue Min")
    h_min_label.place(x=10, y=320, width=100, height=20)
    h_min_display = ttk.Label(window, textvariable=h_min_value)
    h_min_display.place(x=520, y=320, width=50, height=20)
    h_min_trackbar = ttk.Scale(window, from_=0, to=255, orient="horizontal", command=lambda v: h_min_value.set(v))
    h_min_trackbar.place(x=110, y=320, width=400, height=20)

    h_max_label = ttk.Label(window, text="Hue Max")
    h_max_label.place(x=10, y=350, width=100, height=20)
    h_max_display = ttk.Label(window, textvariable=h_max_value)
    h_max_display.place(x=520, y=350, width=50, height=20)
    h_max_trackbar = ttk.Scale(window, from_=0, to=255, orient="horizontal", command=lambda v: h_max_value.set(v))
    h_max_trackbar.place(x=110, y=350, width=400, height=20)

    s_min_label = ttk.Label(window, text="Saturation Min")
    s_min_label.place(x=10, y=380, width=100, height=20)
    s_min_display = ttk.Label(window, textvariable=s_min_value)
    s_min_display.place(x=520, y=380, width=50, height=20)
    s_min_trackbar = ttk.Scale(window, from_=0, to=255, orient="horizontal", command=lambda v: s_min_value.set(v))
    s_min_trackbar.place(x=110, y=380, width=400, height=20)

    s_max_label = ttk.Label(window, text="Saturation Max")
    s_max_label.place(x=10, y=410, width=100, height=20)
    s_max_display = ttk.Label(window, textvariable=s_max_value)
    s_max_display.place(x=520, y=410, width=50, height=20)
    s_max_trackbar = ttk.Scale(window, from_=0, to=255, orient="horizontal", command=lambda v: s_max_value.set(v))
    s_max_trackbar.place(x=110, y=410, width=400, height=20)

    v_min_label = ttk.Label(window, text="Value Min")
    v_min_label.place(x=10, y=440, width=100, height=20)
    v_min_display = ttk.Label(window, textvariable=v_min_value)
    v_min_display.place(x=520, y=440, width=50, height=20)
    v_min_trackbar = ttk.Scale(window, from_=0, to=255, orient="horizontal", command=lambda v: v_min_value.set(v))
    v_min_trackbar.place(x=110, y=440, width=400, height=20)

    v_max_label = ttk.Label(window, text="Value Max")
    v_max_label.place(x=10, y=470, width=100, height=20)
    v_max_display = ttk.Label(window, textvariable=v_max_value)
    v_max_display.place(x=520, y=470, width=50, height=20)
    v_max_trackbar = ttk.Scale(window, from_=0, to=255, orient="horizontal", command=lambda v: v_max_value.set(v))
    v_max_trackbar.place(x=110, y=470, width=400, height=20)

    # Erode size label and spinbox
    erode_label = ttk.Label(window, text="Erode Size")
    erode_label.place(x=720, y=380, width=100, height=20)
    erode_spinbox = ttk.Spinbox(window, from_=1, to=21, increment=2, textvariable=erode_size)
    erode_spinbox.place(x=820, y=380, width=60, height=20)

    # Dilate size label and spinbox
    dilate_label = ttk.Label(window, text="Dilate Size")
    dilate_label.place(x=720, y=420, width=100, height=20)
    dilate_spinbox = ttk.Spinbox(window, from_=1, to=21, increment=2, textvariable=dilate_size)
    dilate_spinbox.place(x=820, y=420, width=60, height=20)

def save_hsv_values(log_func, mode_selection):
    hsv_values = {
        "h_min": float(h_min_value.get()),
        "h_max": float(h_max_value.get()),
        "s_min": float(s_min_value.get()),
        "s_max": float(s_max_value.get()),
        "v_min": float(v_min_value.get()),
        "v_max": float(v_max_value.get())
    }
    mode = mode_selection.get().lower()
    filename = f"{mode}.json"
    with open(filename, 'w') as f:
        json.dump(hsv_values, f, indent=4)
    log_func(f"Saved HSV values to {filename}.")

def load_hsv_values(log_func, mode_selection):
    mode = mode_selection.get().lower()
    filename = f"{mode}.json"
    try:
        with open(filename, 'r') as f:
            hsv_values = json.load(f)
        h_min_value.set(hsv_values["h_min"])
        h_max_value.set(hsv_values["h_max"])
        s_min_value.set(hsv_values["s_min"])
        s_max_value.set(hsv_values["s_max"])
        v_min_value.set(hsv_values["v_min"])
        v_max_value.set(hsv_values["v_max"])
        h_min_trackbar.set(hsv_values["h_min"])
        h_max_trackbar.set(hsv_values["h_max"])
        s_min_trackbar.set(hsv_values["s_min"])
        s_max_trackbar.set(hsv_values["s_max"])
        v_min_trackbar.set(hsv_values["v_min"])
        v_max_trackbar.set(hsv_values["v_max"])
        log_func(f"Loaded HSV values from {filename}.")
    except FileNotFoundError:
        log_func(f"{filename} not found. Please save values first.")

def reset_hsv_values(log_func):
    h_min_value.set(0)
    h_max_value.set(255)
    s_min_value.set(0)
    s_max_value.set(255)
    v_min_value.set(0)
    v_max_value.set(255)
    h_min_trackbar.set(0)
    h_max_trackbar.set(255)
    s_min_trackbar.set(0)
    s_max_trackbar.set(255)
    v_min_trackbar.set(0)
    v_max_trackbar.set(255)
    log_func("HSV values reset to default.")

def get_hsv_min_values():
    # Convert the string values to float, then to int, and finally to uint8
    h_min = int(float(h_min_value.get()))
    s_min = int(float(s_min_value.get()))
    v_min = int(float(v_min_value.get()))
    return np.array([h_min, s_min, v_min], dtype=np.uint8)

def get_hsv_max_values():
    # Convert the string values to float, then to int, and finally to uint8
    h_max = int(float(h_max_value.get()))
    s_max = int(float(s_max_value.get()))
    v_max = int(float(v_max_value.get()))
    return np.array([h_max, s_max, v_max], dtype=np.uint8)

def get_erode_size():
    return int(float(erode_size.get()))

def get_dilate_size():
    return int(float(dilate_size.get()))