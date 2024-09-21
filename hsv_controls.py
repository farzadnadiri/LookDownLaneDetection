import tkinter as tk
from tkinter import ttk
import json
import numpy as np

# Trackbar and value variables dictionaries for left and right cameras
hsv_values = {
    "Left": {
        "h_min_value": None,
        "h_max_value": None,
        "s_min_value": None,
        "s_max_value": None,
        "v_min_value": None,
        "v_max_value": None,
        "erode_size": None,
        "dilate_size": None,
        "trackbars": {}  # Add a dictionary to store references to trackbars
    },
    "Right": {
        "h_min_value": None,
        "h_max_value": None,
        "s_min_value": None,
        "s_max_value": None,
        "v_min_value": None,
        "v_max_value": None,
        "erode_size": None,
        "dilate_size": None,
        "trackbars": {}  # Add a dictionary to store references to trackbars
    }
}

def create_hsv_controls(window, log_func, camera_side, x_offset=0, y_offset=0):
    values = hsv_values[camera_side]
    
    # Initialize the tk.StringVar variables now that we have a root window
    values["h_min_value"] = tk.StringVar(value="0")
    values["h_max_value"] = tk.StringVar(value="255")
    values["s_min_value"] = tk.StringVar(value="0")
    values["s_max_value"] = tk.StringVar(value="255")
    values["v_min_value"] = tk.StringVar(value="0")
    values["v_max_value"] = tk.StringVar(value="255")
    values["erode_size"] = tk.StringVar(value="3")
    values["dilate_size"] = tk.StringVar(value="1")

    # Create HSV controls with trackbars
    values["trackbars"]["h_min"] = create_single_hsv_control(window, "Hue Min", values["h_min_value"], x_offset+10, y_offset+0)
    values["trackbars"]["h_max"] = create_single_hsv_control(window, "Hue Max", values["h_max_value"], x_offset+10, y_offset+30)
    values["trackbars"]["s_min"] = create_single_hsv_control(window, "Saturation Min", values["s_min_value"], x_offset+10, y_offset+60)
    values["trackbars"]["s_max"] = create_single_hsv_control(window, "Saturation Max", values["s_max_value"], x_offset+10, y_offset+90)
    values["trackbars"]["v_min"] = create_single_hsv_control(window, "Value Min", values["v_min_value"], x_offset+10, y_offset+120)
    values["trackbars"]["v_max"] = create_single_hsv_control(window, "Value Max", values["v_max_value"], x_offset+10, y_offset+150)

    # Erode and Dilate size controls
    create_single_spinbox_control(window, "Erode Size", values["erode_size"], x_offset+480, y_offset-70)
    create_single_spinbox_control(window, "Dilate Size", values["dilate_size"], x_offset+480, y_offset-40)

def create_single_hsv_control(window, text, variable, x, y):
    label = ttk.Label(window, text=text)
    label.place(x=x, y=y, width=100, height=20)
    display = ttk.Label(window, textvariable=variable)
    display.place(x=x + 510, y=y, width=50, height=20)
    trackbar = ttk.Scale(window, from_=0, to=255, orient="horizontal", command=lambda v: variable.set(v))
    trackbar.place(x=x + 100, y=y, width=400, height=20)
    return trackbar  # Return trackbar so it can be stored and updated later

def create_single_spinbox_control(window, text, variable, x, y):
    label = ttk.Label(window, text=text)
    label.place(x=x, y=y, width=60, height=20)
    spinbox = ttk.Spinbox(window, from_=1, to=21, increment=2, textvariable=variable)
    spinbox.place(x=x + 60, y=y, width=60, height=20)

def save_hsv_values(log_func, mode_selection, camera_side):
    values = hsv_values[camera_side]
    hsv_vals = {
        "h_min": float(values["h_min_value"].get()),
        "h_max": float(values["h_max_value"].get()),
        "s_min": float(values["s_min_value"].get()),
        "s_max": float(values["s_max_value"].get()),
        "v_min": float(values["v_min_value"].get()),
        "v_max": float(values["v_max_value"].get())
    }
    mode = mode_selection.get().lower()
    filename = f"{camera_side.lower()}_{mode}.json"
    with open(filename, 'w') as f:
        json.dump(hsv_vals, f, indent=4)
    log_func(f"Saved HSV values to {filename}.")

def load_hsv_values(log_func, mode_selection, camera_side):
    values = hsv_values[camera_side]
    mode = mode_selection.get().lower()
    filename = f"{camera_side.lower()}_{mode}.json"
    try:
        with open(filename, 'r') as f:
            hsv_vals = json.load(f)
        for key in hsv_vals:
            values[f"{key}_value"].set(hsv_vals[key])
            # Update the trackbar value
            values["trackbars"][key].set(hsv_vals[key])
        log_func(f"Loaded HSV values from {filename}.")
    except FileNotFoundError:
        log_func(f"{filename} not found. Please save values first.")

def reset_hsv_values(log_func, camera_side):
    values = hsv_values[camera_side]
    for key in ["h_min", "h_max", "s_min", "s_max", "v_min", "v_max"]:
        default_value = "0" if "min" in key else "255"
        values[f"{key}_value"].set(default_value)
        # Update the trackbar value
        values["trackbars"][key].set(default_value)
    log_func(f"HSV values reset to default for {camera_side} camera.")

def get_hsv_min_values(camera_side):
    values = hsv_values[camera_side]
    return np.array([int(float(values["h_min_value"].get())), int(float(values["s_min_value"].get())), int(float(values["v_min_value"].get()))], dtype=np.uint8)

def get_hsv_max_values(camera_side):
    values = hsv_values[camera_side]
    return np.array([int(float(values["h_max_value"].get())), int(float(values["s_max_value"].get())), int(float(values["v_max_value"].get()))], dtype=np.uint8)

def get_erode_size(camera_side):
    return int(float(hsv_values[camera_side]["erode_size"].get()))

def get_dilate_size(camera_side):
    return int(float(hsv_values[camera_side]["dilate_size"].get()))