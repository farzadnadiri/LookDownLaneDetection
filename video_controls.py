import cv2
import numpy as np
from PIL import Image, ImageTk
from video_processing import (
    process_original_frame,
    process_frame_with_convex_hull,
    process_frame_with_masked_lines,
    process_detected_lines_and_distance
)

def update_all_frames(cap, frame1, frame2, frame3, frame4, log_func, distance_label=None, lower_b=None, upper_b=None):
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video from the first frame
        ret, frame = cap.read()

    if ret:
        # Process the same frame with different functions
        processed_frame1 = process_original_frame(frame.copy(), log_func)
        processed_frame2 = process_frame_with_convex_hull(frame.copy(), log_func)
        # Get the HSV range based on the current selection (this would come from the main application)

        processed_frame3 = process_frame_with_masked_lines(frame.copy(), log_func, lower_b, upper_b)
        processed_frame4, distance = process_detected_lines_and_distance(frame.copy(), log_func)
   
        if distance_label:
            distance_label.config(text=f"Distance to lane: {distance:.2f} meters")

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
