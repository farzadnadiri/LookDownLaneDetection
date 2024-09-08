import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import cv2
from hsv_controls import create_hsv_controls, save_hsv_values, load_hsv_values, reset_hsv_values, get_hsv_min_values, get_hsv_max_values, get_erode_size, get_dilate_size
from video_controls import update_all_frames
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from pid_controller import PIDController, update_steering
import matplotlib.pyplot as plt  # Importing pyplot as plt

pid_controller = PIDController(kp=1.0, ki=0.1, kd=0.01, integral_limit=10)
dt = 0.1  # Time step for PID calculation

new_left_lane = 0
new_right_lane = 0
new_steering_adjustment = 0
new_actual_car_position = 0
new_projected_car_position = 0
new_histogram_left = None
new_histogram_right = None
def log_message(textbox, message):
    textbox.insert(tk.END, message + "\n")
    textbox.see(tk.END)

def log_func(message):
    log_message(log_console, message)

# Window setup
window = tk.Tk()
window.title("Lane Detection using Look Down Method")
window.geometry('1360x1550')  # Adjusted height for better layout

# Video capture objects for left and right cameras
cap_left = cv2.VideoCapture('samples\\sample0\\sample_left.mp4')
cap_right = cv2.VideoCapture('samples\\sample0\\sample_right.mp4')

# Function to create video frames and labels dynamically
def create_frame_and_label(x, y, text):
    frame = ttk.Label(window)
    frame.place(x=x, y=y, width=320, height=240)
    label = ttk.Label(window, text=text)
    label.place(x=x, y=y+250, width=320, height=20)
    return frame, label

def draw_lanes_and_car(canvas, right_lane_distance, left_lane_distance, steering_adjustment):
    canvas.delete("all")  # Clear previous drawings

    # Define lane positions and car position
    canvas_width = 450
    canvas_height = 150
    lane_width = 200
    
    # Center of the canvas
    center_x = canvas_width // 2
    
    # Fixed lane positions
    left_lane_x = (canvas_width - lane_width) // 2
    right_lane_x = (canvas_width + lane_width) // 2
    
    # Adjust the car's horizontal position based on steering adjustment
    car_x = center_x - (right_lane_distance - left_lane_distance)
    steering_wheel_x = center_x + steering_adjustment

    # Draw left lane (fixed position)
    canvas.create_line(left_lane_x, 0, left_lane_x, canvas_height, fill="blue", width=5)
    
    # Draw right lane (fixed position)
    canvas.create_line(right_lane_x, 0, right_lane_x, canvas_height, fill="blue", width=5)
    
    canvas.create_line(center_x, 0, center_x, canvas_height, fill="gray", width=1, dash=(2, 4))

    # Draw the car as a rectangle centered between the lanes
    car_y = canvas_height // 2 + 10
    car_width = 50
    car_height = 80
    canvas.create_rectangle(car_x - car_width // 2, car_y - car_height // 2, car_x + car_width // 2, car_y + car_height // 2, fill="green")

    # Draw the steering wheel 
    steering_wheel_y = canvas_height // 2 - 40
    steering_wheel_width = 50
    steering_wheel_height = 10
    canvas.create_rectangle(steering_wheel_x - steering_wheel_width // 2, steering_wheel_y - steering_wheel_height // 2, steering_wheel_x + steering_wheel_width // 2, steering_wheel_y + steering_wheel_height // 2, fill="orange")
     # === Add Legend to the right side of the canvas ===

    legend_x = canvas_width - 50  # X-position for the legend
    legend_y_start = 30            # Starting Y-position for the first legend item
    legend_spacing = 20            # Spacing between legend items

    # Blue lane lines
    canvas.create_rectangle(legend_x, legend_y_start, legend_x + 10, legend_y_start + 10, fill="blue")
    canvas.create_text(legend_x + 20, legend_y_start + 5, anchor="w", text="Lane Lines", fill="black")

    # Green car
    canvas.create_rectangle(legend_x, legend_y_start + legend_spacing, legend_x + 10, legend_y_start + 10 + legend_spacing, fill="green")
    canvas.create_text(legend_x + 20, legend_y_start + 5 + legend_spacing, anchor="w", text="Car", fill="black")

    # Orange steering wheel
    canvas.create_rectangle(legend_x, legend_y_start + 2 * legend_spacing, legend_x + 10, legend_y_start + 10 + 2 * legend_spacing, fill="orange")
    canvas.create_text(legend_x + 20, legend_y_start + 5 + 2 * legend_spacing, anchor="w", text="Steering Wheel", fill="black")

    # Gray lane center
    canvas.create_rectangle(legend_x, legend_y_start + 3 * legend_spacing, legend_x + 10, legend_y_start + 10 + 3 * legend_spacing, fill="gray")
    canvas.create_text(legend_x + 20, legend_y_start + 5 + 3 * legend_spacing, anchor="w", text="Lane Center", fill="black")

# Function to open a new window for displaying real-time graphs
def open_chart_window():
    chart_window = tk.Toplevel(window)  # Create a new window
    chart_window.title("Real-time Graphs")
    chart_window.geometry("1200x800")  # Set the size of the new window

    # Create a Matplotlib figure with 4 subplots (2x2 grid)
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.tight_layout(pad=5.0)

    # Create empty line plots for each graph

    # Graph 1: Left and Right lane distances
    x_data = np.linspace(0, 10, 100)
    left_lane_data = np.zeros_like(x_data)
    right_lane_data = np.zeros_like(x_data)
    left_line, = axs[0, 0].plot(x_data, left_lane_data, color='red', label="Left Lane Distance")
    right_line, = axs[0, 0].plot(x_data, right_lane_data, color='blue', label="Right Lane Distance")
    axs[0, 0].set_title("Left and Right Lane Distances")
    axs[0, 0].set_xlabel("Time")
    axs[0, 0].set_ylabel("Distance")
    axs[0, 0].legend()

    # Graph 2: Steering wheel adjustment
    steering_data = np.zeros_like(x_data)
    error_data = np.zeros_like(x_data)
    steering_line, = axs[0, 1].plot(x_data, steering_data, color='green', label="Steering Adjustment")
    error_line, = axs[0, 1].plot(x_data, error_data, color='red', label="left and right Error")
    axs[0, 1].set_title("Steering Wheel Adjustment")
    axs[0, 1].set_xlabel("Time")
    axs[0, 1].set_ylabel("Adjustment Value")
    axs[0, 1].legend()

    # Graph 3: Actual car position and projected car position
    actual_car_data = np.zeros_like(x_data)
    projected_car_data = np.zeros_like(x_data)
    actual_car_line, = axs[1, 0].plot(x_data, actual_car_data, color='orange', label="Actual Car Position")
    projected_car_line, = axs[1, 0].plot(x_data, projected_car_data, color='purple', label="Projected Car Position")
    axs[1, 0].set_title("Car Position (Actual vs Projected)")
    axs[1, 0].set_xlabel("Time")
    axs[1, 0].set_ylabel("Position")
    axs[1, 0].legend()

    # Graph 4: Left and Right histograms with lane base markers
    histogram_x = np.arange(len(new_histogram_left))
    
    left_hist_line, = axs[1, 1].plot(histogram_x, new_histogram_left, color='blue', label="Left Histogram")
    right_hist_line, = axs[1, 1].plot(histogram_x, new_histogram_right, color='red', label="Right Histogram")
    left_lane_base_line = axs[1, 1].axvline(x=0, color='blue', linestyle='--', label='Left Peak')
    right_lane_base_line = axs[1, 1].axvline(x=0, color='red', linestyle='--', label='Right Peak')
    
    axs[1, 1].set_title("Left and Right Frame Histograms with Lane Base Peaks")
    axs[1, 1].set_xlabel("Pixel Intensity")
    axs[1, 1].set_ylabel("Frequency")
    axs[1, 1].legend()

    # Embed the Matplotlib figure into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_graph(new_left_lane, new_right_lane, new_steering_adjustment, new_actual_car_position, new_projected_car_position,new_histogram_left, new_histogram_right):
        # Update lane distances
        left_lane_data[:-1] = left_lane_data[1:]  # Shift data to the left
        right_lane_data[:-1] = right_lane_data[1:]
        left_lane_data[-1] = new_left_lane  # Add new data
        right_lane_data[-1] = new_right_lane
        left_line.set_ydata(left_lane_data)
        right_line.set_ydata(right_lane_data)

        # Update steering adjustment
        steering_data[:-1] = steering_data[1:]
        steering_data[-1] = new_steering_adjustment
        steering_line.set_ydata(steering_data)
        error = right_lane_data - left_lane_data
        error_line.set_ydata(error)

        # Update actual and projected car position
        actual_car_data[:-1] = actual_car_data[1:]
        projected_car_data[:-1] = projected_car_data[1:]
        actual_car_data[-1] = new_actual_car_position
        projected_car_data[-1] = new_projected_car_position
        actual_car_line.set_ydata(error)
        projected_car_line.set_ydata(error + steering_data)

           # Update histograms and lane base markers
        if new_histogram_left is not None and new_histogram_right is not None:
            left_hist_line.set_ydata(new_histogram_left)
            right_hist_line.set_ydata(new_histogram_right)

            # Update lane base markers using np.argmax to find the peaks
            left_lane_base = np.argmax(new_histogram_left)
            right_lane_base = np.argmax(new_histogram_right)
            left_lane_base_line.set_xdata([left_lane_base])
            right_lane_base_line.set_xdata([right_lane_base])

        # Redraw the canvas with the updated plots
        axs[0, 0].relim()
        axs[0, 0].autoscale_view()
        axs[0, 1].relim()
        axs[0, 1].autoscale_view()
        axs[1, 0].relim()
        axs[1, 0].autoscale_view()
        axs[1, 1].relim()
        axs[1, 1].autoscale_view()
        canvas.draw()

    def update_graph_periodically():
        # Update graphs with new data
        update_graph(new_left_lane, new_right_lane, new_steering_adjustment, new_actual_car_position, new_projected_car_position, new_histogram_left, new_histogram_right)
        # Call this function again after 500 ms
        chart_window.after(500, update_graph_periodically)

    # Start the periodic updates
    update_graph_periodically()

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
log_console.place(x=10, y=870, width=670, height=150)

# canvas drawing
canvas = tk.Canvas(window, width=650, height=150, bg="white")
canvas.place(x=690, y=870)

# open the real-time graph window
btn_open_chart = ttk.Button(window, text="Open Graphs", command=open_chart_window)
btn_open_chart.place(x=1230, y=880, width=100, height=30)

# Function to repeatedly call update_all_frames
def schedule_update():
    if window.winfo_exists():
        distance_left, histogram_left = update_all_frames(cap_left, left_frame1, left_frame2, left_frame3, left_frame4, log_func, distance_label_left,
                      get_hsv_min_values("Left"), get_hsv_max_values("Left"), get_erode_size("Left"), get_dilate_size("Left"),"Left",alg_selection_left.get())
        distance_right, histogram_right = update_all_frames(cap_right, right_frame1, right_frame2, right_frame3, right_frame4, log_func, distance_label_right,
                      get_hsv_min_values("Right"), get_hsv_max_values("Right"), get_erode_size("Right"), get_dilate_size("Right"),"Right",alg_selection_right.get())
        if distance_left is not None and distance_right is not None:
            global new_left_lane
            global new_right_lane
            global new_steering_adjustment
            global new_histogram_left
            global new_histogram_right

            new_left_lane = distance_left
            new_right_lane = distance_right
            new_histogram_left = histogram_left
            new_histogram_right = histogram_right
            error = distance_right - distance_left

            steering_adjustment = update_steering(distance_right/10, distance_left/10, pid_controller, dt)
            new_steering_adjustment = -10 * steering_adjustment
            draw_lanes_and_car(canvas, distance_right/10, distance_left/10, steering_adjustment)
            log_func(f"distance error:{error} steering_adjustment: {steering_adjustment}")
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
