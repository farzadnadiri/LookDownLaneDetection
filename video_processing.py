import cv2
import numpy as np

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

def process_detected_lines_and_distance(frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size):
    cleaned_frame = remove_car(frame, exclude_percentage=25)  # Use remove_car function
    mask = process_frame_with_mask(cleaned_frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size)
    lines, distance = detect_horizontal_lanes(mask, frame)  # Detect horizontal lanes
    return lines, distance

def process_frame_with_mask(frame, log_func, lowerb, upperb, erode_kernel_size=5, dilate_kernel_size=5):
    # Convert frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask based on the provided HSV ranges
    mask = cv2.inRange(hsv_frame, lowerb, upperb)
    
    # Create kernels for erosion and dilation
    erode_kernel = np.ones((erode_kernel_size, erode_kernel_size), np.uint8)
    dilate_kernel = np.ones((dilate_kernel_size, dilate_kernel_size), np.uint8)

    # Apply erosion followed by dilation (commonly known as an opening operation)
    mask = cv2.erode(mask, erode_kernel, iterations=1)
    mask = cv2.dilate(mask, dilate_kernel, iterations=1)

    # Apply the mask to create the binary frame
    binary_frame = cv2.bitwise_and(frame, frame, mask=mask)
    
    return binary_frame

def detect_horizontal_lanes(binary_frame, line_image):
    # Apply Canny edge detection
    edges = cv2.Canny(binary_frame, 50, 150, apertureSize=3)

    # Use Hough Line Transform to detect lines
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=150)

    distances_to_bottom = []

    if lines is not None:
        for rho, theta in lines[:, 0]:
            # Only consider horizontal lines (theta close to π/2 or 3π/2)
            if (np.pi / 2 - np.pi / 18) < theta < (np.pi / 2 + np.pi / 18) or (3 * np.pi / 2 - np.pi / 18) < theta < (3 * np.pi / 2 + np.pi / 18):
                # Calculate the coordinates for the line
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                # Draw the line on the image
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Calculate the vertical distance from the line to the bottom of the frame
                frame_height = binary_frame.shape[0]

                # Choose one y-coordinate (y1 or y2) to calculate distance
                distance_to_bottom = frame_height - max(y1, y2)
                distances_to_bottom.append(distance_to_bottom)

    # Calculate the average distance if any lines were detected
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
