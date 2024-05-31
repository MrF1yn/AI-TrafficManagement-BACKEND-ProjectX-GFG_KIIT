import cv2
import numpy as np

# Specify file paths
weights_path = r'C:\Users\KIIT0001\Downloads\Smart_traffic_management_system\backup2.1\traffic_management\signin\Vehicle_Count\yolov3.weights'
config_path = r'C:\Users\KIIT0001\Downloads\Smart_traffic_management_system\backup2.1\traffic_management\signin\Vehicle_Count\yolov3.cfg'
names_path = r'C:\Users\KIIT0001\Downloads\Smart_traffic_management_system\backup2.1\traffic_management\signin\Vehicle_Count\coco.names'

def count_vehicles(image_path):
    # Load YOLO
    net = cv2.dnn.readNet(weights_path, config_path)
    classes = []
    with open(names_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Load image
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Error loading image at path: {image_path}")
    else:
        height, width, channels = image.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Lists to store class IDs, confidences, and bounding boxes
        class_ids = []
        confidences = []
        boxes = []

        # Identify vehicles and store their class IDs, confidences, and bounding boxes
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.7 and class_id in [2, 3, 5, 7]:  # Adjust confidence threshold and class IDs as needed
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Store class ID, confidence, and bounding box coordinates
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([center_x, center_y, w, h])

        # Apply Non-Maximum Suppression (NMS) to eliminate redundant detections
        indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.7, nms_threshold=0.5)
        if len(indices) > 0:
            # Draw bounding boxes and labels for each vehicle
            for i in indices.flatten():
                box = boxes[i]
                center_x, center_y, w, h = box
                class_id = class_ids[i]
                confidence = confidences[i]

                # Draw bounding box around the vehicle
                cv2.rectangle(image, (center_x - w // 2, center_y - h // 2), (center_x + w // 2, center_y + h // 2),
                              (0, 255, 0), 2)

#                 # Label the vehicle
#                 label = f'Vehicle: {classes[class_id]}'
#                 cv2.putText(image, label, (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 255, 255), 6)

                 # Display the total number of vehicles in the top left corner of the image
                num_vehicles = len(indices)
                cv2.putText(image, f'Total Vehicles: {num_vehicles}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Resize the output image to (800, 600)
            image = cv2.resize(image, (800, 600))

            # Display the number of vehicles detected
            num_vehicles = len(indices)
            # print(f"Number of vehicles detected: {num_vehicles}")

            # Display the image with bounding boxes, labels, and number of vehicles
            # cv2.imshow("Image with Vehicles", image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            return num_vehicles
        else:
            print("No vehicles detected.")
        
# Example usage:
def main():
    image_path = r'C:\Users\KIIT\Downloads\vehicle-count\data\demo5.jpg'  # Path to the image
    number = count_vehicles(image_path)
    print(number)

if __name__ == "__main__":
    main()