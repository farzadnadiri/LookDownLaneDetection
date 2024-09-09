import cv2
import numpy as np
import matplotlib.pyplot as plt

# Video capture for input video
video = cv2.VideoCapture("samples\\sample3\\front_camera.mp4")
is_frame_available, frame_image = video.read()

# Placeholder function for trackbars
def empty_callback(x):
    pass

# Creating window and trackbars for HSV adjustments
cv2.namedWindow("HSV_Adjustments")
cv2.createTrackbar("Low - H", "HSV_Adjustments", 0, 255, empty_callback)
cv2.createTrackbar("Low - S", "HSV_Adjustments", 0, 255, empty_callback)
cv2.createTrackbar("Low - V", "HSV_Adjustments", 180, 255, empty_callback)
cv2.createTrackbar("High - H", "HSV_Adjustments", 38, 255, empty_callback)
cv2.createTrackbar("High - S", "HSV_Adjustments", 61, 255, empty_callback)
cv2.createTrackbar("High - V", "HSV_Adjustments", 255, 255, empty_callback)

# Enable interactive mode for matplotlib
plt.ion()

# Create a Matplotlib figure for real-time plots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Create empty line plots for real-time updates
x_data = np.linspace(0, 10, 100)
left_lane_data = np.zeros_like(x_data)
right_lane_data = np.zeros_like(x_data)
left_line, = axs[0, 0].plot(x_data, left_lane_data, color='red', label="Left Lane Distance")
right_line, = axs[0, 0].plot(x_data, right_lane_data, color='blue', label="Right Lane Distance")
axs[0, 0].set_title("Left and Right Lane Distances")
axs[0, 0].set_xlabel("Time")
axs[0, 0].set_ylabel("Distance")
axs[0, 0].legend()

# Create histogram x_data to match the shape of lane_histogram (half the width of the frame, e.g., 400)
histogram_x_data = np.arange(400)
new_histogram_left = np.zeros_like(histogram_x_data)
new_histogram_right = np.zeros_like(histogram_x_data)
left_hist_line, = axs[1, 1].plot(histogram_x_data, new_histogram_left, color='blue', label="Left Histogram")
right_hist_line, = axs[1, 1].plot(histogram_x_data, new_histogram_right, color='red', label="Right Histogram")
axs[1, 1].set_title("Lane Histograms")
axs[1, 1].set_xlabel("Pixels")
axs[1, 1].set_ylabel("Intensity")
axs[1, 1].legend()

# Function to update the charts
def update_graphs(left_lane_pos, right_lane_pos, histogram_left, histogram_right):
    # Ensure the lane positions are non-negative
    left_lane_pos = max(0, left_lane_pos)
    right_lane_pos = max(0, right_lane_pos)

    # Shift data for real-time updates
    left_lane_data[:-1] = left_lane_data[1:]
    right_lane_data[:-1] = right_lane_data[1:]
    left_lane_data[-1] = left_lane_pos
    right_lane_data[-1] = right_lane_pos

    left_hist_line.set_ydata(histogram_left)
    right_hist_line.set_ydata(histogram_right)

    # Update line plots with new data
    left_line.set_ydata(left_lane_data)
    right_line.set_ydata(right_lane_data)

    # Rescale the axes automatically
    axs[0, 0].relim()
    axs[0, 0].autoscale_view()
    
    axs[1, 1].relim()
    axs[1, 1].autoscale_view()

    # Redraw the canvas
    fig.canvas.draw()
    fig.canvas.flush_events()

# Loop through video frames
while is_frame_available:
    is_frame_available, frame_image = video.read()
    if not is_frame_available:
        break
    resized_frame = cv2.resize(frame_image, (800, 600))  # Change frame size to 800x600

    # Defining points for perspective transformation (adjusted for the new size)
    top_left = (200, 334)  # Adjusted to match new frame size
    bottom_left = (0, 500)
    top_right = (570, 334)
    bottom_right = (800, 500)

    # Drawing circles on the selected points for reference
    cv2.circle(resized_frame, top_left, 5, (0, 0, 255), -1)
    cv2.circle(resized_frame, bottom_left, 5, (0, 0, 255), -1)
    cv2.circle(resized_frame, top_right, 5, (0, 0, 255), -1)
    cv2.circle(resized_frame, bottom_right, 5, (0, 0, 255), -1)

    # Perspective transformation from road to bird’s eye view
    src_points = np.float32([top_left, bottom_left, top_right, bottom_right])
    dst_points = np.float32([[0, 0], [0, 600], [800, 0], [800, 600]])  # Updated for 800x600 resolution
    
    # Transformation matrix to change perspective
    transform_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    bird_view_frame = cv2.warpPerspective(resized_frame, transform_matrix, (800, 600))

    # Convert frame to HSV for thresholding
    hsv_bird_view = cv2.cvtColor(bird_view_frame, cv2.COLOR_BGR2HSV)
    
    # Fetching values from the trackbars
    low_h = cv2.getTrackbarPos("Low - H", "HSV_Adjustments")
    low_s = cv2.getTrackbarPos("Low - S", "HSV_Adjustments")
    low_v = cv2.getTrackbarPos("Low - V", "HSV_Adjustments")
    high_h = cv2.getTrackbarPos("High - H", "HSV_Adjustments")
    high_s = cv2.getTrackbarPos("High - S", "HSV_Adjustments")
    high_v = cv2.getTrackbarPos("High - V", "HSV_Adjustments")
    
    # Setting HSV thresholds
    lower_hsv = np.array([low_h, low_s, low_v])
    upper_hsv = np.array([high_h, high_s, high_v])
    binary_mask = cv2.inRange(hsv_bird_view, lower_hsv, upper_hsv)
    kernel = np.ones((5, 5), np.uint8)  # Define a 5x5 kernel, you can adjust the size
    
    # Erode the binary mask to remove noise
    binary_mask = cv2.erode(binary_mask, kernel, iterations=1)

    # Dilate the binary mask to expand the white regions
    binary_mask = cv2.dilate(binary_mask, kernel, iterations=2)

    # Generating histogram for lane base detection
    lane_histogram = np.sum(binary_mask[binary_mask.shape[0]//2:, :], axis=0)
    center_point = int(lane_histogram.shape[0] / 2)
    left_lane_base = np.argmax(lane_histogram[:center_point])
    right_lane_base = np.argmax(lane_histogram[center_point:]) + center_point

    # Sliding window technique
    y_coordinate = 590  # Adjusted for new frame height
    left_lane_positions = []
    right_lane_positions = []

    sliding_window_mask = binary_mask.copy()

    while y_coordinate > 0:
        # Left lane search window
        left_region = binary_mask[y_coordinate-40:y_coordinate, left_lane_base-50:left_lane_base+50]
        contours_left, _ = cv2.findContours(left_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours_left:
            moments_left = cv2.moments(contour)
            if moments_left["m00"] != 0:
                center_x_left = int(moments_left["m10"] / moments_left["m00"])
                center_y_left = int(moments_left["m01"] / moments_left["m00"])
                left_lane_positions.append(left_lane_base - 50 + center_x_left)
                left_lane_base = left_lane_base - 50 + center_x_left

        # Right lane search window
        right_region = binary_mask[y_coordinate-40:y_coordinate, right_lane_base-50:right_lane_base+50]
        contours_right, _ = cv2.findContours(right_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours_right:
            moments_right = cv2.moments(contour)
            if moments_right["m00"] != 0:
                center_x_right = int(moments_right["m10"] / moments_right["m00"])
                center_y_right = int(moments_right["m01"] / moments_right["m00"])
                right_lane_positions.append(right_lane_base - 50 + center_x_right)
                right_lane_base = right_lane_base - 50 + center_x_right

        # Drawing sliding windows on the mask
        cv2.rectangle(sliding_window_mask, (left_lane_base-50, y_coordinate), 
                      (left_lane_base+50, y_coordinate-40), (255, 255, 255), 2)
        cv2.rectangle(sliding_window_mask, (right_lane_base-50, y_coordinate), 
                      (right_lane_base+50, y_coordinate-40), (255, 255, 255), 2)
        y_coordinate -= 40

    # Update the real-time graphs
    update_graphs(left_lane_base, right_lane_base, lane_histogram[:center_point], lane_histogram[center_point:])

    # Displaying all frames and masks
    cv2.imshow("Original Frame", resized_frame)
    cv2.imshow("Bird’s Eye View", bird_view_frame)
    cv2.imshow("Lane Detection Threshold", binary_mask)
    cv2.imshow("Lane Detection with Sliding Windows", sliding_window_mask)

    # Exit loop on pressing 'ESC'
    if cv2.waitKey(10) == 27:
        break

# Disable interactive mode after the loop is finished
plt.ioff()

# Show the final plot
plt.show()
