import cv2
import numpy as np
from datetime import datetime

fgbg = cv2.createBackgroundSubtractorMOG2()
LEARNING_RATE = -1   
THRESHOLD = 10000
def motion_detection_processing(frame, frame_number, crud):
    """
    Processes a video frame to detect motion using background subtraction and morphological operations.

    Parameters:
    frame (numpy.ndarray): The current video frame.
    frame_number (int): The index of the current frame.

    Returns:
    dict: A dictionary containing the processed motion mask frame.
          {"frame": motion_mask}
    """
    # Apply the background subtractor to get the motion mask
    motion_mask = fgbg.apply(frame, learningRate=LEARNING_RATE)
    
    # Apply morphological operations to get rid of noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_OPEN, kernel)
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, kernel)
    
    # Apply thresholding to get a binary image
    ret, motion_mask = cv2.threshold(motion_mask, 127, 255, cv2.THRESH_BINARY)

    # Count non-zero pixels
    # non_zero_count = np.count_nonzero(motion_mask)

    # print(non_zero_count)
    
    # # Check if the count exceeds the threshold
    # if non_zero_count > THRESHOLD:
    #     crud["update"](f"motion_detected/{datetime.now()}", {non_zero_count: non_zero_count})

    return {"frame": motion_mask}