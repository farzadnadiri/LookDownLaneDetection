"""Module does the processing unit based on input frame."""

import cv2
import numpy as np

def process_original_frame(frame, log_func):
    # log_func("Processing original frame")
    return frame

def process_frame_with_convex_hull(frame, log_func):
    # log_func("Processing frame with convex hull")
    return frame

def process_frame_with_masked_lines(frame, log_func, lowerb, upperb):

    # log_func("Processing frame with masked lines")
    hsv_frame =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask based on the provided HSV ranges
    mask = cv2.inRange(hsv_frame, lowerb, upperb)

    # Apply the mask to create the binary frame
    binary_frame = cv2.bitwise_and(frame, frame, mask=mask)

    return binary_frame

def process_detected_lines_and_distance(frame, log_func):
    # log_func("Processing frame with detected lines and distance calculation")
    distance = 0  # Placeholder for actual distance calculation
    return frame, distance
