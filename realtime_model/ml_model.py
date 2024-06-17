import base64

import cv2
import numpy as np
import time
from collections import defaultdict
import json


# Load YOLO
def load_yolo():
    net = cv2.dnn.readNet("yolo/yolov3.weights", "yolo/yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    with open("yolo/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return net, output_layers, classes


# Detect objects
def detect_objects(img, net, output_layers):
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    return outs


# Get bounding boxes
def get_bounding_boxes(outs, width, height, classes):
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and classes[class_id] == 'car':
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    return boxes, confidences, indexes


# Function to display multiple video feeds with car detection and traffic signal logic
def display_videos_with_traffic_management(video_paths, window_names, net, output_layers, classes):
    caps = [cv2.VideoCapture(video) for video in video_paths]
    fps = [cap.get(cv2.CAP_PROP_FPS) for cap in caps]
    car_counts = defaultdict(int)
    start_time = time.time()

    while True:
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video if it ends
                ret, frame = cap.read()

            height, width, channels = frame.shape
            outs = detect_objects(frame, net, output_layers)
            boxes, confidences, indexes = get_bounding_boxes(outs, width, height, classes)

            # Draw bounding boxes and count cars
            car_count = 0
            for j in range(len(boxes)):
                if j in indexes:
                    x, y, w, h = boxes[j]
                    label = str(classes[0])
                    color = (0, 255, 0)
                    car_count += 1
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Update car count for the lane
            car_counts[window_names[i]] = car_count

            # Display car count
            cv2.putText(frame, f'Cars: {car_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow(window_names[i], frame)

            # Delay to match the video's frame rate
            time.sleep(1 / fps[i])

        # Check if 10 seconds have passed
        if time.time() - start_time > 10:
            start_time = time.time()
            # Determine the lane with the most cars
            max_lane = max(car_counts, key=car_counts.get)

            print(f"Lane with most cars: {max_lane}")
            print(car_counts)

            # Simulate traffic signal change (for visualization purpose, we can print or update a display)
            for lane in window_names:
                if lane == max_lane:
                    print(f"Green Light for {lane}")
                else:
                    print(f"Red Light for {lane}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()


net, output_layers, classes = load_yolo()


# Function to send data to socket with car detection and traffic signal logic
def predict(video_paths, socket):
    window_names = ['Lane 1', 'Lane 2', 'Lane 3', 'Lane 4']
    caps = [cv2.VideoCapture(video) for video in video_paths]
    fps = [cap.get(cv2.CAP_PROP_FPS) for cap in caps]
    car_counts = {}
    car_counts_number = defaultdict(int)
    start_time = time.time()

    while True:
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video if it ends
                ret, frame = cap.read()

            height, width, channels = frame.shape
            outs = detect_objects(frame, net, output_layers)
            boxes, confidences, indexes = get_bounding_boxes(outs, width, height, classes)

            # Draw bounding boxes and count cars
            car_count = 0
            for j in range(len(boxes)):
                if j in indexes:
                    x, y, w, h = boxes[j]
                    label = str(classes[0])
                    color = (0, 255, 0)
                    car_count += 1
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Update car count for the lane
            # ret, buffer = cv2.imencode('.jpg', frame)
            car_counts_number[window_names[i]] = car_count
            car_counts[window_names[i]] = {}
            car_counts[window_names[i]]['count'] = car_count
            car_counts[window_names[i]]['frame'] = frame

            # Display car count
            # cv2.putText(frame, f'Cars: {car_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # cv2.imshow(window_names[i], frame)

            # Delay to match the video's frame rate
            time.sleep(1 / fps[i])

        # Check if 10 seconds have passed
        if time.time() - start_time > 2:
            start_time = time.time()
            # Determine the lane with the most cars
            max_lane = max(car_counts_number, key=car_counts_number.get)
            data = []

            print(f"Lane with most cars: {max_lane} ")
            print(car_counts)

            # Simulate traffic signal change (for visualization purpose, we can print or update a display)
            for idx, lane in enumerate(window_names):
                data.append({})
                data[idx]['car_count'] = car_counts[lane]['count']
                data[idx]['fps'] = fps[idx]
                data[idx]['time'] = start_time
                ret, buffer = cv2.imencode('.jpg', car_counts[lane]['frame'])
                data[idx]['frame'] = str(base64.b64encode(buffer), "utf-8")
                if lane == max_lane:
                    print(f"Green Light for {lane}")
                    data[idx]['stop'] = False
                else:
                    print(f"Red Light for {lane}")
                    data[idx]['stop'] = True

            socket.send(text_data=json.dumps(data))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()


# Load YOLO model


# Video file paths
video_paths_1 = ['./video/vid1.avi', './video/vid2.avi', './video/vid3.avi', './video/vid4.avi']
video_paths_2 = ['./video/vid1.avi', './video/vid2.avi', './video/vid3.avi', './video/vid4.avi']
# window_names = {'Int1': ['Lane 1', 'Lane 2', 'Lane 3', 'Lane 4'], 'Int2': ['Lane 1', 'Lane 2', 'Lane 3', 'Lane 4']}

# Display the video feeds with car detection and traffic management
# display_videos_with_traffic_management(video_paths_1, window_names['Int1'], net, output_layers, classes)
# display_videos_with_traffic_management(video_paths_2, window_names['Int2'], net, output_layers, classes)
