import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_original_frame(frame, log_func):
    # log_func("Processing original frame")
    return frame

def process_frame_with_convex_hull(frame, log_func):
    # log_func("Processing frame with convex hull")
    cleaned_frame = remove_car(frame, exclude_percentage=25)  # Use remove_car function

    return cleaned_frame

def process_frame_with_masked_lines(frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size):
    cleaned_frame = remove_car(frame, exclude_percentage=25)  # Use remove_car function
    return process_frame_with_mask(cleaned_frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size)

def process_detected_lines_and_distance(frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size, algorithm):
    cleaned_frame = remove_car(frame, exclude_percentage=25)  # Use remove_car function
    mask = process_frame_with_mask(cleaned_frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size)
    histogram = cleaned_frame
    if algorithm == "hough":
        lines, distance = detect_horizontal_lanes(mask, frame)  # Detect horizontal lanes
    else:
        lines, lane_fitx, ploty, distance, histogram = detect_horizontal_lane_with_sliding_window(
        mask, frame)
    
    return lines, distance , histogram

def process_frame_with_mask(frame, log_func, lowerb, upperb, erode_kernel_size=5, dilate_kernel_size=5):
    # Convert frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask based on the provided HSV ranges
    mask = cv2.inRange(hsv_frame, lowerb, upperb)
    
    # Apply Gaussian Blur to reduce noise and smooth the mask
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Create kernels for erosion and dilation
    erode_kernel = np.ones((erode_kernel_size, erode_kernel_size), np.uint8)
    dilate_kernel = np.ones((dilate_kernel_size, dilate_kernel_size), np.uint8)

    # Apply erosion followed by dilation (opening operation)
    mask = cv2.erode(mask, erode_kernel, iterations=2)
    mask = cv2.dilate(mask, dilate_kernel, iterations=2)
    
    return mask

def detect_horizontal_lanes(binary_frame, line_image):
    # Apply Canny edge detection
    edges = cv2.Canny(binary_frame, 50, 150, apertureSize=3)

    # Use Probabilistic Hough Line Transform for better control
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=500, maxLineGap=50)

    distances_to_bottom = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Calculate slope to filter out non-horizontal lines
            slope = (y2 - y1) / (x2 - x1 + 1e-6)  # Avoid division by zero
            if abs(slope) < 0.1:  # Near horizontal
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                frame_height = binary_frame.shape[0]
                distance_to_bottom = frame_height - max(y1, y2)
                distances_to_bottom.append(distance_to_bottom)

    average_distance = np.mean(distances_to_bottom) if distances_to_bottom else None
    return line_image, average_distance

def remove_car(frame, exclude_percentage=20):
    """
    Remove the bottom portion of the frame to exclude the car.
    """
    # Get the frame dimensions
    height, width = frame.shape[:2]

    # Calculate the height of the area to exclude
    exclude_height = int(height * exclude_percentage / 100)

    # Create a mask to exclude the bottom of the frame
    mask = np.zeros_like(frame, dtype=np.uint8)
    mask[:height-exclude_height, :] = 255  # Keep only the upper part of the image

    # Apply the mask to the frame
    masked_frame = cv2.bitwise_and(frame, mask)
    
    return masked_frame

def detect_horizontal_lane_with_sliding_window(binary_frame, out_img, n_windows=9, margin=30, minpix=1000):
    """
    Detect horizontal lanes using sliding window method and calculate the distance to the lane.

    Args:
        binary_frame (numpy.ndarray): Binary image of the road.
        out_img (numpy.ndarray): Image to draw the detected lane on.
        n_windows (int): Number of sliding windows.
        margin (int): Width of the windows +/- margin.
        minpix (int): Minimum number of pixels found to recenter window.

    Returns:
        out_img (numpy.ndarray): Image with detected lane drawn.
        lane_fity (numpy.ndarray): Y values for the lane line.
        plotx (numpy.ndarray): X values for plotting the lane line.
        distance_to_lane (float): Distance from the vehicle to the lane line.
    """
    # Take a histogram of the image to find the lane line
    histogram = np.sum(binary_frame, axis=1)
    # Apply a simple moving average (smoothing filter) to reduce noise

 # Check if the peak of the histogram is less than the threshold
    if np.max(histogram) < 50000: # thershhold to cancel algorithm
        return out_img, None, None, None, histogram
    # Find the peak of the histogram, which indicates the position of the lane line
    lane_base = np.argmax(histogram)

    if 0==1: # adjust it if you want plot
        plt.figure(figsize=(10, 5))
        plt.plot(histogram, label='Histogram of pixel sums')
        plt.axvline(x=lane_base, color='red', linestyle='--', label=f'Peak at row {lane_base}')
        plt.title('Histogram of Image Row Intensities with Peak Highlighted')
        plt.xlabel('Row Index')
        plt.ylabel('Sum of Pixel Values')
        plt.legend()
        plt.show()
    # Set width of windows
    window_width = int(binary_frame.shape[1] // n_windows)
    
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_frame.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    # Current position to be updated for each window
    lane_current = lane_base

    # Create empty list to receive lane line pixel indices
    lane_inds = []

    # Step through the windows one by one
    for window in range(n_windows):
        # Identify window boundaries in x and y (and top and bottom)
        win_x_low = binary_frame.shape[1] - (window + 1) * window_width
        win_x_high = binary_frame.shape[1] - window * window_width
        win_y_low = lane_current - margin
        win_y_high = lane_current + margin

        # Draw the window on the visualization image
        cv2.rectangle(out_img, (win_x_low, win_y_low), (win_x_high, win_y_high), (0, 255, 0), 2)

        # Identify the nonzero pixels in x and y within the window
        good_lane_inds = ((nonzerox >= win_x_low) & (nonzerox < win_x_high) & 
                          (nonzeroy >= win_y_low) & (nonzeroy < win_y_high)).nonzero()[0]
        
        # Append these indices to the list
        lane_inds.append(good_lane_inds)

        # If found > minpix pixels, recenter next window on their mean position
        if len(good_lane_inds) > minpix:
            lane_current = int(np.mean(nonzeroy[good_lane_inds]))

    # Concatenate the arrays of indices
    lane_inds = np.concatenate(lane_inds)

    # Extract lane line pixel positions
    lanex = nonzerox[lane_inds]
    laney = nonzeroy[lane_inds]

    # Check if we have enough points to fit a line
    if len(lanex) == 0 or len(laney) == 0:
        # Not enough points to fit a polynomial
        return out_img, None, None, None, None  # or other default values

    # Fit a second order polynomial to the lane line pixels
    lane_fit = np.polyfit(lanex, laney, 2)

    # Generate x and y values for plotting
    plotx = np.linspace(0, binary_frame.shape[1] - 1, binary_frame.shape[1])
    lane_fity = lane_fit[0] * plotx**2 + lane_fit[1] * plotx + lane_fit[2]

    
    distance_to_lane = binary_frame.shape[0] - lane_fity[-1]  # Distance from the vehicle to the lane line

    # Highlight the lane pixels
    out_img[nonzeroy[lane_inds], nonzerox[lane_inds]] = [255, 0, 0]

    return out_img, lane_fity, plotx, distance_to_lane, histogram
