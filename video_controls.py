import cv2
import numpy as np
from PIL import Image, ImageTk
from video_processing import (
    process_original_frame,
    process_frame_with_convex_hull,
    process_frame_with_masked_lines,
    process_detected_lines_and_distance
)

def update_all_frames(cap, frame1, frame2, frame3, frame4, log_func, distance_label=None, lower_b=None, upper_b=None, erode_size=None, dilate_size=None, side="", algorithm="hough"):
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video from the first frame
        ret, frame = cap.read()

    if ret:
        # Ensure erode_size and dilate_size are not None and are valid integers
        erode_kernel_size = erode_size if erode_size is not None else 3
        dilate_kernel_size = dilate_size if dilate_size is not None else 1
        
        # Ensure kernel sizes are odd and at least 1
        erode_kernel_size = max(1, erode_kernel_size if erode_kernel_size % 2 == 1 else erode_kernel_size + 1)
        dilate_kernel_size = max(1, dilate_kernel_size if dilate_kernel_size % 2 == 1 else dilate_kernel_size + 1)

        # Process the same frame with different functions
        processed_frame1 = process_original_frame(frame.copy(), log_func)
        processed_frame2 = process_frame_with_convex_hull(frame.copy(), log_func)
        processed_frame3 = process_frame_with_masked_lines(frame.copy(), log_func, lower_b, upper_b, erode_kernel_size, dilate_kernel_size)
        processed_frame4, distance = process_detected_lines_and_distance(frame.copy(), log_func, lower_b, upper_b, erode_kernel_size, dilate_kernel_size,algorithm)
   
        if distance_label:
            if distance is not None:
                distance_label.config(text=f"Distance to lane ({side}): {int(distance)} px")
            else:
                distance_label.config(text="Distance to lane ({side}): N/A")
        
        # Display each processed frame in the corresponding label
        display_frame(frame1, processed_frame1)
        display_frame(frame2, processed_frame2)
        display_frame(frame3, processed_frame3)
        display_frame(frame4, processed_frame4)

def display_frame(label, frame):
    frame = cv2.resize(frame, (320, 240))
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_img = Image.fromarray(frame_rgb)
    frame_tk = ImageTk.PhotoImage(image=frame_img)
    label.imgtk = frame_tk
    label.config(image=frame_tk)
