import requests
import numpy as np
import base64
import torch
import cv2
import pygame
from datetime import datetime
import os

def numpy_to_bytes(array):
    metadata = {
        'dtype': str(array.dtype),
        'shape': array.shape
    }
    data = array.tobytes()
    metadata_encoded = base64.b64encode(str(metadata).encode('utf-8')).decode('utf-8')
    data_encoded = base64.b64encode(data).decode('utf-8')
    return {"metadata": metadata_encoded, "data": data_encoded}

def bytes_to_numpy(data):
    metadata_bstring = data['metadata']
    data_bstring = data['data']
    metadata_decoded = eval(base64.b64decode(metadata_bstring).decode('utf-8'))
    data_decoded = base64.b64decode(data_bstring)
    array = np.frombuffer(data_decoded, dtype=metadata_decoded['dtype']).reshape(metadata_decoded['shape'])
    return array

def tensor_to_bytes(tensor):
    # Convert the PyTorch dtype to a string format that NumPy understands
    numpy_dtype_str = str(tensor.numpy().dtype)
    
    metadata = {
        'dtype': numpy_dtype_str,
        'shape': tensor.shape
    }
    data = tensor.numpy().tobytes()
    metadata_encoded = base64.b64encode(str(metadata).encode('utf-8')).decode('utf-8')
    data_encoded = base64.b64encode(data).decode('utf-8')
    return {"metadata": metadata_encoded, "data": data_encoded}

def bytes_to_tensor(data):
    metadata_bstring = data['metadata']
    data_bstring = data['data']
    metadata_decoded = eval(base64.b64decode(metadata_bstring).decode('utf-8'))
    data_decoded = base64.b64decode(data_bstring)
    
    # Convert the dtype string back into a NumPy dtype
    numpy_dtype = np.dtype(metadata_decoded['dtype'])
    
    array = np.frombuffer(data_decoded, dtype=numpy_dtype).reshape(metadata_decoded['shape'])
    tensor = torch.from_numpy(array)
    return tensor

def convert_dict_values_to_bytes(d):
    if d is None: return None

    result = {}
    for key, value in d.items():
        if isinstance(value, np.ndarray):
            result[key] = numpy_to_bytes(value)
        elif isinstance(value, torch.Tensor):
            result[key] = tensor_to_bytes(value)
        else:
            result[key] = value  # Leave other types unchanged
    return result

def convert_dict_values_to_tensor(d):
    result = {}
    for key, value in d.items():
        result[key] = bytes_to_tensor(value)
    return result

def convert_dict_values_to_numpy(d):
    result = {}
    for key, value in d.items():
        result[key] = bytes_to_numpy(value)
    return result

def calibration_gui():
    # Initialize pygame
    pygame.init()

    # Set up the screen for fullscreen display
    infoObject = pygame.display.Info()
    screen_width, screen_height = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Calibration")

    # Set colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Define calibration points
    calibration_points = [
        (screen_width // 2, screen_height // 2),  # Center
        (screen_width // 2, 25),  # Top center near edge
        (screen_width - 25, 25),  # Top right near edge
        (screen_width - 25, screen_height // 2),  # Middle right near edge
        (screen_width - 25, screen_height - 25),  # Bottom right near edge
        (screen_width // 2, screen_height - 25),  # Bottom center near edge
        (25, screen_height - 25),  # Bottom left near edge
        (25, screen_height // 2),  # Middle left near edge
        (25, 25)  # Top left near edge
    ]

    # Set up camera
    cap = cv2.VideoCapture(0)  # Adjust the device index based on your camera

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Video recording setup
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('calibration.mp4', fourcc, 20.0, (640, 480))

    current_point_index = 0
    is_clicked = False
    click_times = []
    click_frames = []
    clicked_points = []
    start_time = datetime.now()

    # Game loop
    running = True
    clock = pygame.time.Clock()

    frame_count = 0
    gt = []
    frame_times = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to quit
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos
                    point_x, point_y = calibration_points[current_point_index]
                    distance = np.sqrt((point_x - mouse_x) ** 2 + (point_y - mouse_y) ** 2)
                    if distance < 25:  # Sensitivity radius
                        is_clicked = True
                        clicked_time = datetime.now()
                    else:
                        is_clicked = False
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and is_clicked:
                    elapsed_time = (datetime.now() - clicked_time).total_seconds()
                    if elapsed_time >= 3:
                        click_times.append(int((datetime.now() - start_time).total_seconds() * 1000))
                        clicked_points.append(calibration_points[current_point_index])
                        click_frames.append(frame_count)
                        current_point_index = (current_point_index + 1) % len(calibration_points)
                    is_clicked = False

        # Webcam frame capture
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        out.write(frame)  # Write frame to video file

        # Clear screen
        screen.fill(BLACK)

        # Draw the current calibration point
        if current_point_index < len(calibration_points) and len(click_times) < len(calibration_points):
            point_x, point_y = calibration_points[current_point_index]
            if is_clicked:
                size = 24*(1 - (int((datetime.now() - clicked_time).total_seconds()*1000) % 3000) / 3000)
                pygame.draw.circle(screen, GREEN, (point_x, point_y), size)
                if is_clicked:
                    elapsed_time = (datetime.now() - clicked_time).total_seconds()
                    if elapsed_time >= 3:
                        click_times.append(int((datetime.now() - start_time).total_seconds() * 1000))
                        clicked_points.append(calibration_points[current_point_index])
                        click_frames.append(frame_count)
                        current_point_index = (current_point_index + 1) % len(calibration_points)
                        is_clicked = False
            else:
                pygame.draw.circle(screen, RED, (point_x, point_y), 25)  # Larger circle for easier targeting
        else:
            running = False

        pygame.display.flip()
        clock.tick(30)
        frame_count += 1
        gt.append(calibration_points[current_point_index])
        frame_times.append(int((datetime.now() - start_time).total_seconds() * 1000))

    # Cleanup
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    pygame.quit()
    
    ranges = [] # list of tuples (start_frame, end_frame) for each point
    ratio = frame_count / click_times[-1]
    for i in range(len(click_frames)):
        start_frame = int((click_times[i] - 3000) * ratio)
        ranges.append((start_frame, click_frames[i]))
    
    # update calibration.mp4 to only include the frames from start_frame to end_frame for each point
    cap = cv2.VideoCapture('calibration.mp4')
    frames = []
    
    frame_num = 0
    # dataPoints = []
    time_slices = []
    for i in range(len(ranges)):
        start_frame, end_frame = ranges[i]
        while frame_num < start_frame:
            ret, frame = cap.read()
            frame_num += 1
        while frame_num <= end_frame:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
            # dataPoints.append(
            #     {
            #         "PoT": [gt[i][0], gt[i][1]],
            #         "time": frame_times[frame_num]
            #     }
            # )
            frame_num += 1
        time_slices.append(len(frames))
    
    cap.release()
    out = cv2.VideoWriter('calibration.mp4', fourcc, 20.0, (640, 480))
    for frame in frames:
        out.write(frame)
    out.release()
    
    del cap, out, frames, frame
    
    return "calibration.mp4", screen_width, screen_height, calibration_points, time_slices

class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def calibrate(self):
        video_path, w, h, calibration_points, time_slices = calibration_gui()
        function_endpoint = "video/calibrate"
        with open(video_path, 'rb') as f:
            response = requests.post(
                f'http://vytalgazeapilb-1065850898.us-east-1.elb.amazonaws.com/{function_endpoint}',
                # f'http://127.0.0.1:8000/{function_endpoint}',
                params={"api_key": self.api_key, "width": w, "height": h, "points": str(calibration_points), "time_slices": str(time_slices)},
                files = {"file": f},
                timeout=1000, 
            )
            
            try:
                result = bytes_to_tensor(response.json())
            except:
                result = response.json()
                
        try:
            # os.remove(video_path)
            pass
        except:
            pass
        
        return result
                   
    def predict_from_video(self, video_path: str, calib_mat: np.array = None):    
        function_endpoint = "video/handle_video"

        with open(video_path, 'rb') as f:
            calib_mat_bytes = tensor_to_bytes(torch.from_numpy(calib_mat)) if calib_mat is not None else None
            response = requests.post(
                f'http://vytalgazeapilb-1065850898.us-east-1.elb.amazonaws.com/{function_endpoint}',
                # f'http://127.0.0.1:8000/{function_endpoint}',
                params={"api_key": self.api_key} if calib_mat is None else {"api_key": self.api_key, "calib_mat": str(calib_mat_bytes)},
                files = {"file": f},
                timeout=1000,
            )
            
            try:
                result = {}
                for key, value in response.json().items():
                    result[key] = bytes_to_tensor(value)
            except:
                result = response.json()

        return result

    