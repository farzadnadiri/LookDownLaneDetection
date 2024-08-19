import cv2
import numpy as np

def process_original_frame(frame, log_func):
    # log_func("Processing original frame")
    return frame

def process_frame_with_convex_hull(frame, log_func):
    # log_func("Processing frame with convex hull")
    cleaned_frame = remove_right_side(frame, exclude_percentage=25)

    return cleaned_frame

def process_frame_with_masked_lines(frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size):
    cleaned_frame = remove_right_side(frame, exclude_percentage=25)
    return process_frame_with_mask(cleaned_frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size)


def process_detected_lines_and_distance(frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size):
    cleaned_frame = remove_right_side(frame, exclude_percentage=25)
    mask = process_frame_with_mask(cleaned_frame, log_func, lowerb, upperb, erode_kernel_size, dilate_kernel_size)
    lines, distance = detect_vertical_lanes(mask, frame)
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

def detect_vertical_lanes(binary_frame, line_image):
    # Apply Canny edge detection
    edges = cv2.Canny(binary_frame, 50, 150, apertureSize=3)

    # Use Hough Line Transform to detect lines
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=150)

    distances_to_right = []

    if lines is not None:
        for rho, theta in lines[:, 0]:
            # Only consider vertical lines (theta close to 0 or pi)
            if np.abs(theta) < np.pi / 18 or np.abs(theta - np.pi) < np.pi / 18:
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

                # Calculate the horizontal distance from the line to the right side of the frame
                frame_width = binary_frame.shape[1]

                # Choose one x-coordinate (x1 or x2) to calculate distance
                distance_to_right = frame_width - max(x1, x2)
                distances_to_right.append(distance_to_right)

    # Calculate the average distance if any lines were detected
    average_distance = np.mean(distances_to_right) if distances_to_right else None
    return line_image, average_distance

def remove_right_side(frame, exclude_percentage=20):
    # Get the frame dimensions
    height, width = frame.shape[:2]

    # Calculate the width of the area to exclude
    exclude_width = int(width * exclude_percentage / 100)

    # Create a mask to exclude the right side of the frame
    mask = np.zeros_like(frame, dtype=np.uint8)
    mask[:, :width-exclude_width] = 255  # Keep only the left part of the image

    # Apply the mask to the frame
    masked_frame = cv2.bitwise_and(frame, mask)
    
    return masked_frame